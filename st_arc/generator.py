"""Tools for prompting OpenAI to produce SolarTopps-ready HTML articles."""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence


SYSTEM_PROMPT = textwrap.dedent(
    """
    You are Senior Solar Content Strategist, an expert copywriter for SolarTopps.com.
    Always produce polished, SEO-optimized solar articles tailored to the SolarTopps
    brand. Respond with raw HTML only – do not include Markdown fences, comments, or
    explanations. Ensure the output follows the provided structure and contains at
    least 1,500 words.
    """
)

MASTER_PROMPT = textwrap.dedent(
    """
    Let's play a very interesting game: from now on you will play the role [Senior Solar
    Content Strategist], a new version of AI model trained to write SEO-optimized,
    expert-level solar blog articles tailored for the brand SolarTopps.com.

    You must write a minimum 1500-word article in raw HTML, using SEO formatting compatible
    with Yoast SEO, SEMRush, and Google Search Console. Format the content using clean
    paragraph blocks, properly nested H1, H2, and H3 tags, a strong title, a meta
    description (under 155 characters), and include schema markup in JSON-LD. All HTML
    must be compatible with the WordPress post editor. Ensure you strictly follow the
    structure below:

    [introduction]: - (H1 and strong introduction paragraph using the keyword)
    [meta_data]: - (HTML meta description, title, and slug block)
    [main_content]: - (1500+ words of body content, SEO-optimized, with headings and structured flow)
    [data_visualization]: - (Simple data chart in HTML+CSS or a placeholder <div> with alt text)
    [inline_citations]: - (At least one external and one internal link, formatted as part of paragraph text)
    [schema_block]: - (JSON-LD structured data block for BlogPosting)
    [final_html]: - (Complete raw HTML code block ready for WordPress input)

    The primary keyword is: "{keyword}". Ensure it appears in the title, first paragraph,
    at least one H2 heading, and a minimum of 5 times across the body content. Keep the
    tone authoritative yet approachable, aligned with SolarTopps brand voice. Use active
    voice in over 90%% of sentences, transition words in over 30%%, limit passive voice to
    under 10%%, and keep complex words under 20%%. Provide one outbound citation and one
    SolarTopps internal link.

    Reference article or notes:
    {reference_text}

    Secondary keywords: {secondary_keywords}
    Focus topic or theme: {focus_topic}
    Chart data guidance: {chart_data}
    Preferred slug: {slug}
    Preferred meta title: {meta_title}
    Preferred meta description: {meta_description}

    Craft the content so that Yoast's readability and SEO checklists are green. Use
    descriptive anchor text for links and ensure the schema markup is valid JSON-LD.
    Finish by echoing the complete HTML document only.
    """
)


@dataclass
class ArticleRequest:
    """Parameters required to build the SolarTopps article prompt."""

    keyword: str
    reference_text: str
    secondary_keywords: Sequence[str] | None = None
    focus_topic: Optional[str] = None
    chart_data: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    slug: Optional[str] = None

    def render_secondary_keywords(self) -> str:
        if not self.secondary_keywords:
            return "None provided"
        return ", ".join(self.secondary_keywords)

    def render_chart_data(self) -> str:
        if not self.chart_data:
            return "Use inferred data if helpful"
        return self.chart_data

    def render_focus_topic(self) -> str:
        return self.focus_topic or "Highlight SolarTopps' ROI expertise"

    def render_meta_title(self) -> str:
        return self.meta_title or "Generate an SEO-friendly meta title"

    def render_meta_description(self) -> str:
        return self.meta_description or "Write a compelling meta description under 155 characters"

    def render_slug(self) -> str:
        return self.slug or "Generate an SEO-friendly slug"


def fetch_reference_source(
    *,
    reference_url: Optional[str] = None,
    reference_file: Optional[str] = None,
    reference_text: Optional[str] = None,
) -> str:
    """Load the reference material from a URL, file, or direct text block."""

    if reference_text:
        return reference_text

    if reference_file:
        path = Path(reference_file)
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:  # noqa: PLE0704
            raise RuntimeError(f"Failed to read reference file '{path}': {exc}") from exc

    if reference_url:
        import requests

        response = requests.get(reference_url, timeout=30)
        response.raise_for_status()
        return response.text

    raise ValueError("Provide at least one of reference_url, reference_file, or reference_text")


class SolarArticleGenerator:
    """Generate SolarTopps articles using the OpenAI Responses API."""

    def __init__(self, *, model: str = "gpt-4.1-mini", temperature: float = 0.7, api_key: Optional[str] = None):
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def build_prompt(self, request: ArticleRequest) -> str:
        """Render the templated master prompt with request-specific data."""

        return MASTER_PROMPT.format(
            keyword=request.keyword,
            reference_text=request.reference_text,
            secondary_keywords=request.render_secondary_keywords(),
            focus_topic=request.render_focus_topic(),
            chart_data=request.render_chart_data(),
            slug=request.render_slug(),
            meta_title=request.render_meta_title(),
            meta_description=request.render_meta_description(),
        )

    def generate(self, request: ArticleRequest) -> str:
        """Send the prompt to OpenAI and return the resulting HTML."""

        prompt = self.build_prompt(request)
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
        )
        article = response.output_text
        return strip_code_fences(article)


def strip_code_fences(article: str) -> str:
    """Remove Markdown code fences if the model accidentally adds them."""

    trimmed = article.strip()
    if trimmed.startswith("```") and trimmed.endswith("```"):
        lines = trimmed.splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:-1]).strip()
        return ""
    return trimmed
