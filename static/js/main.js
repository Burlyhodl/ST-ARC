// ST-ARC Blog Generator - Frontend JavaScript

// State management
let currentResult = null;

// DOM Elements
const form = document.getElementById('generatorForm');
const tabButtons = document.querySelectorAll('.tab-button');
const inputPanels = document.querySelectorAll('.input-panel');
const fileInput = document.getElementById('contentFile');
const fileInfo = document.getElementById('fileInfo');
const loadingOverlay = document.getElementById('loadingOverlay');
const resultsSection = document.getElementById('resultsSection');
const generateBtn = document.getElementById('generateBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupTabSwitching();
    setupFileUpload();
    setupFormSubmission();
    setupResultActions();
});

// Tab Switching
function setupTabSwitching() {
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const method = button.dataset.method;
            
            // Update active tab
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update active panel
            inputPanels.forEach(panel => panel.classList.remove('active'));
            const activePanel = document.querySelector(`[data-panel="${method}"]`);
            if (activePanel) {
                activePanel.classList.add('active');
            }
        });
    });
}

// File Upload
function setupFileUpload() {
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) {
            fileInfo.classList.add('hidden');
            return;
        }
        
        // Display file info
        fileInfo.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
        fileInfo.classList.remove('hidden');
        
        // Read file content
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Failed to upload file');
            }
            
            const data = await response.json();
            // Store content for later use
            fileInput.dataset.content = data.content;
            
        } catch (error) {
            console.error('File upload error:', error);
            showToast('Failed to read file', 'error');
        }
    });
}

// Form Submission
function setupFormSubmission() {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Get active input method
        const activeTab = document.querySelector('.tab-button.active');
        const inputMethod = activeTab.dataset.method;
        
        // Gather form data
        const formData = {
            inputMethod: inputMethod,
            keyword: document.getElementById('keyword').value.trim(),
            secondaryKeywords: document.getElementById('secondaryKeywords').value.trim(),
            slug: document.getElementById('slug').value.trim(),
            dataPoints: document.getElementById('dataPoints').value.trim()
        };
        
        // Get content based on input method
        if (inputMethod === 'text') {
            formData.content = document.getElementById('contentText').value.trim();
            if (!formData.content) {
                showToast('Please enter some reference content', 'error');
                return;
            }
        } else if (inputMethod === 'url') {
            formData.url = document.getElementById('contentUrl').value.trim();
            if (!formData.url) {
                showToast('Please enter a URL', 'error');
                return;
            }
        } else if (inputMethod === 'file') {
            if (!fileInput.dataset.content) {
                showToast('Please upload a file first', 'error');
                return;
            }
            formData.content = fileInput.dataset.content;
        }
        
        // Validate keyword
        if (!formData.keyword) {
            showToast('Please enter a target keyword', 'error');
            return;
        }
        
        // Show loading
        showLoading(true);
        generateBtn.disabled = true;
        
        try {
            // Call API
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to generate blog post');
            }
            
            const result = await response.json();
            currentResult = result;
            
            // Display results
            displayResults(result);
            showToast('Blog post generated successfully!', 'success');
            
        } catch (error) {
            console.error('Generation error:', error);
            showToast(error.message || 'Failed to generate blog post', 'error');
        } finally {
            showLoading(false);
            generateBtn.disabled = false;
        }
    });
}

// Display Results
function displayResults(result) {
    // Update metadata
    document.getElementById('resultTitle').textContent = result.title;
    document.getElementById('resultSlug').textContent = result.slug;
    document.getElementById('resultMetaDesc').textContent = result.meta_description;
    document.getElementById('resultWordCount').textContent = `${result.word_count} words`;
    
    // Update HTML preview
    document.getElementById('htmlContent').textContent = result.content;
    
    // Show results section
    resultsSection.classList.remove('hidden');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Result Actions
function setupResultActions() {
    // Preview button
    document.getElementById('previewBtn').addEventListener('click', () => {
        if (!currentResult) return;
        
        // Open preview in new window
        const previewWindow = window.open('', '_blank');
        previewWindow.document.write(currentResult.content);
        previewWindow.document.close();
    });
    
    // Copy button
    document.getElementById('copyBtn').addEventListener('click', async () => {
        if (!currentResult) return;
        
        try {
            await navigator.clipboard.writeText(currentResult.content);
            showToast('HTML copied to clipboard!', 'success');
        } catch (error) {
            console.error('Copy error:', error);
            showToast('Failed to copy to clipboard', 'error');
        }
    });
    
    // Download button
    document.getElementById('downloadBtn').addEventListener('click', async () => {
        if (!currentResult) return;
        
        try {
            const filename = `blog_${currentResult.slug}.html`;
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    html: currentResult.content,
                    filename: filename
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to download file');
            }
            
            // Download file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showToast('File downloaded successfully!', 'success');
            
        } catch (error) {
            console.error('Download error:', error);
            showToast('Failed to download file', 'error');
        }
    });
    
    // Toggle preview
    const toggleBtn = document.getElementById('togglePreviewBtn');
    const htmlPreview = document.getElementById('htmlPreview');
    const toggleIcon = document.getElementById('toggleIcon');
    
    toggleBtn.addEventListener('click', () => {
        const isHidden = htmlPreview.classList.contains('hidden');
        
        if (isHidden) {
            htmlPreview.classList.remove('hidden');
            toggleIcon.textContent = '▲';
            toggleBtn.childNodes[1].textContent = ' Hide Full HTML Preview';
        } else {
            htmlPreview.classList.add('hidden');
            toggleIcon.textContent = '▼';
            toggleBtn.childNodes[1].textContent = ' Show Full HTML Preview';
        }
    });
    
    // Reset button
    document.getElementById('resetBtn').addEventListener('click', () => {
        // Reset form
        form.reset();
        fileInfo.classList.add('hidden');
        delete fileInput.dataset.content;
        
        // Hide results
        resultsSection.classList.add('hidden');
        htmlPreview.classList.add('hidden');
        
        // Reset state
        currentResult = null;
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Utility Functions
function showLoading(show) {
    if (show) {
        loadingOverlay.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
    }
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastIcon = document.getElementById('toastIcon');
    const toastMessage = document.getElementById('toastMessage');
    
    // Set icon based on type
    const icons = {
        success: '✓',
        error: '✗',
        warning: '⚠',
        info: 'ℹ'
    };
    
    toastIcon.textContent = icons[type] || icons.info;
    toastMessage.textContent = message;
    
    // Set type class
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 5000);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!generateBtn.disabled) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});
