# SEO Compliance Guide

## Yoast SEO Green Score Requirements

This generator ensures all content meets Yoast SEO's green score requirements for both SEO and Readability.

## SEO Analysis Checklist

### ✅ Keyphrase in Title
- **Requirement**: Target keyword must appear in the page title
- **Implementation**: Primary keyword is automatically inserted in the generated title
- **Example**: "Tesla Powerwall Installation Cost Arizona: Expert Analysis..."

### ✅ Keyphrase in Meta Description
- **Requirement**: Target keyword must appear in meta description
- **Implementation**: Meta description is auto-generated with keyword
- **Length**: 155-160 characters (optimal for SERP display)
- **Example**: "Discover Tesla Powerwall installation cost Arizona insights..."

### ✅ Keyphrase in Introduction
- **Requirement**: Target keyword must appear in first paragraph
- **Implementation**: First paragraph always contains the keyword in bold
- **Position**: Within first 150 words

### ✅ Keyphrase in Subheading
- **Requirement**: Keyword must appear in at least one H2 heading
- **Implementation**: First H2 always includes the full keyword
- **Example**: "Understanding Tesla Powerwall Installation Cost Arizona: The Fundamentals"

### ✅ Keyphrase Density
- **Requirement**: 0.5% - 2.5% keyword density
- **Implementation**: Keyword appears 5+ times in 1500+ word content
- **Typical Result**: 0.8% - 1.2% density (optimal range)

### ✅ Text Length
- **Requirement**: Minimum 300 words
- **Implementation**: Generates 1500+ words consistently
- **Benefit**: More comprehensive than competitors

### ✅ Outbound Links
- **Requirement**: At least one external link to authoritative source
- **Implementation**: 3+ authority links automatically added
- **Sources**: .gov, .edu, industry organizations (NREL, DOE, SEIA)

### ✅ Meta Description Length
- **Requirement**: 120-160 characters
- **Implementation**: Always 155-160 characters
- **SEO Benefit**: Full description visible in search results

### ✅ URL Slug
- **Requirement**: URL contains target keyword
- **Implementation**: Slug auto-generated from title with keyword
- **Format**: lowercase, hyphen-separated, no special characters

## Readability Analysis Checklist

### ✅ Subheading Distribution
- **Requirement**: Subheadings every 300 words or less
- **Implementation**: H2 every 250-300 words, H3 for subsections
- **Count**: 6-8 H2 headings, 2-4 H3 headings

### ✅ Paragraph Length
- **Requirement**: Paragraphs under 150 words
- **Implementation**: Paragraphs limited to 2-5 lines (40-80 words)
- **Benefit**: Improved scannability and mobile readability

### ✅ Sentence Length
- **Requirement**: Average sentence length under 20 words
- **Implementation**: Sentences typically 15-25 words
- **Benefit**: Easier comprehension for diverse audiences

### ✅ Transition Words
- **Requirement**: 30%+ of sentences contain transition words
- **Implementation**: Strategic use of: however, therefore, additionally, furthermore, consequently, moreover
- **Examples**: 
  - "However, the core concepts are straightforward..."
  - "Additionally, modern systems often include..."
  - "Furthermore, most systems pay for themselves..."

### ✅ Passive Voice
- **Requirement**: Less than 10% passive voice
- **Implementation**: Active voice used throughout
- **Examples**:
  - ❌ Passive: "Energy is stored by the battery"
  - ✅ Active: "The battery stores energy"

### ✅ Consecutive Sentences
- **Requirement**: No more than 3 consecutive sentences starting with the same word
- **Implementation**: Varied sentence structure and opening words
- **Benefit**: More engaging, natural-sounding content

### ✅ Flesch Reading Ease
- **Requirement**: Score of 60+ (fairly easy to read)
- **Implementation**: Clear language, short sentences, common words
- **Target Audience**: High school reading level (accessible to 80%+ of adults)

## Technical SEO Elements

### ✅ Structured Data (Schema.org)
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Article Title",
  "description": "Meta description",
  "author": {...},
  "publisher": {...},
  "datePublished": "ISO 8601 date",
  "dateModified": "ISO 8601 date",
  "mainEntityOfPage": {...}
}
```

**Benefits**:
- Enhanced SERP appearance (rich snippets)
- Better understanding by search engines
- Potential for featured snippets
- Voice search optimization

### ✅ HTML5 Semantic Structure
- Proper heading hierarchy (H1 → H2 → H3)
- Article tags for blog content
- Semantic HTML elements
- ARIA labels where appropriate

### ✅ Mobile Optimization
- Responsive design (viewport meta tag)
- Touch-friendly elements
- Fast-loading content
- No horizontal scrolling required

### ✅ Font and Typography
- **Primary Font**: Montserrat (web-safe, Google Fonts)
- **Line Height**: 1.8 (optimal for readability)
- **Font Sizes**: 
  - H1: 2.5em
  - H2: 1.8em
  - H3: 1.4em
  - Body: 1em (16px default)

## Link Building Strategy

### External Links (Authority Building)
- **Quantity**: 3-5 per article
- **Quality**: .gov, .edu, industry leaders
- **Anchor Text**: Descriptive, natural-sounding
- **Examples**:
  - ❌ "Click here for more info"
  - ✅ "According to the U.S. Department of Energy"

### Internal Links (Site Architecture)
- Not automatically generated (requires site context)
- Recommended: 2-4 internal links per article
- Link to related blog posts and service pages

## Content Quality Signals

### ✅ Expertise Indicators
- Industry terminology used correctly
- Specific data and statistics
- Balanced perspective
- Professional tone

### ✅ Freshness Signals
- Current year mentioned in content
- Recent dates in schema markup
- Up-to-date information and trends

### ✅ Depth and Comprehensiveness
- 1500+ words (comprehensive coverage)
- Multiple perspectives addressed
- Common questions answered
- Actionable information provided

### ✅ User Engagement Elements
- Data visualization (increases time on page)
- Bullet points (improves scannability)
- Clear headings (aids navigation)
- Logical flow (reduces bounce rate)

## WordPress Plugin Compatibility

### Yoast SEO Plugin
- ✅ Meta description auto-populated
- ✅ Focus keyphrase pre-optimized
- ✅ Readability score: GREEN
- ✅ SEO score: GREEN

### Rank Math
- ✅ Compatible with structured data
- ✅ Optimized for all key metrics
- ✅ Schema markup included

### All in One SEO
- ✅ Meta tags properly formatted
- ✅ Social media markup compatible
- ✅ XML sitemap ready

## Testing Your Generated Content

### Manual Checks
1. **Copy content to WordPress**
2. **Install Yoast SEO plugin**
3. **Set focus keyphrase**
4. **Check SEO score** (should be green)
5. **Check readability score** (should be green)
6. **Preview in mobile view**
7. **Test data visualization rendering**

### Tools to Use
- **Yoast SEO**: In-editor scoring
- **Google Search Console**: Post-publication monitoring
- **SEMrush**: Keyword ranking tracking
- **PageSpeed Insights**: Load time verification
- **Schema Markup Validator**: Test JSON-LD

## Common Yoast SEO Issues (Avoided)

### ❌ Issues This Generator Prevents:
- Keyword not in title → ✅ Always in title
- Meta description too long → ✅ 155-160 chars
- No outbound links → ✅ 3+ authority links
- Paragraphs too long → ✅ 2-5 line paragraphs
- Too much passive voice → ✅ Active voice used
- Not enough subheadings → ✅ Heading every 250-300 words
- Content too short → ✅ 1500+ words
- No transition words → ✅ 30%+ usage
- Keyword density wrong → ✅ 0.8-1.2% optimal

## Monitoring and Optimization

### Post-Publication
1. Monitor in Google Search Console
2. Track keyword rankings in SEMrush
3. Check Core Web Vitals
4. Monitor bounce rate and time on page
5. Update content annually for freshness

### Continuous Improvement
- Update statistics annually
- Refresh schema dates
- Add new sections as industry evolves
- Monitor competitor content
- Adjust based on user feedback

## Credits

This SEO compliance ensures content meets the standards outlined in:
- Yoast SEO documentation
- Google Search Quality Guidelines
- Schema.org specifications
- Web Content Accessibility Guidelines (WCAG)

For more information, visit https://godofprompt.ai/gpts
