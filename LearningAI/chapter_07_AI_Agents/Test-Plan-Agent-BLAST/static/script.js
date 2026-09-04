/* Jira Test Plan Generator - JavaScript */

// Store the current result
let currentResult = null;

// DOM Elements
const generatorForm = document.getElementById('generatorForm');
const issueKeyInput = document.getElementById('issueKey');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners
generatorForm.addEventListener('submit', handleFormSubmit);
document.getElementById('downloadMarkdown').addEventListener('click', downloadMarkdown);
document.getElementById('downloadJSON').addEventListener('click', downloadJSON);
document.getElementById('copyJSON').addEventListener('click', copyJSON);

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    const issueKey = issueKeyInput.value.trim().toUpperCase();
    if (!issueKey) {
        showError('Please enter an issue ID');
        return;
    }

    // Hide previous results/errors
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';

    // Show loading
    loadingSection.style.display = 'block';

    try {
        // Call API
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ issueKey })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate test plan');
        }

        // Store result and display
        currentResult = data;
        displayResults(data, issueKey);

    } catch (error) {
        showError(error.message);
    } finally {
        loadingSection.style.display = 'none';
    }
}

/**
 * Display results
 */
function displayResults(data, issueKey) {
    // Metadata
    document.getElementById('resultIssueKey').textContent = data.issueKey || issueKey;
    document.getElementById('resultTitle').textContent = data.metadata?.title || 'N/A';
    document.getElementById('resultType').textContent = data.metadata?.issueType || 'N/A';
    document.getElementById('resultPriority').textContent = data.metadata?.priority || 'N/A';
    document.getElementById('resultGenerated').textContent = new Date().toLocaleString();

    // Objective
    document.getElementById('resultObjective').textContent = data.objective || 'No objective provided';

    // Coverage
    if (data.coverage) {
        const totalCriteria = data.coverage.totalAcceptanceCriteria || 0;
        const covered = data.coverage.coveredCriteria || 0;
        const percent = totalCriteria > 0 ? Math.round((covered / totalCriteria) * 100) : 0;

        document.getElementById('coverageTotalCriteria').textContent = totalCriteria;
        document.getElementById('coverageCovered').textContent = covered;
        document.getElementById('coveragePercent').textContent = percent + '%';

        const coverageBar = document.getElementById('coverageBar');
        coverageBar.style.width = percent + '%';
    }

    // Test case counts
    if (data.testPlan) {
        document.getElementById('countHappyPath').textContent = (data.testPlan.happyPath || []).length;
        document.getElementById('countNegative').textContent = (data.testPlan.negative || []).length;
        document.getElementById('countEdgeCases').textContent = (data.testPlan.edgeCases || []).length;
        document.getElementById('countRegression').textContent = (data.testPlan.regression || []).length;
    }

    // Priority distribution
    if (data.distribution) {
        document.getElementById('priorityHigh').textContent = data.distribution.high || 0;
        document.getElementById('priorityMedium').textContent = data.distribution.medium || 0;
        document.getElementById('priorityLow').textContent = data.distribution.low || 0;
    }

    // Quality flags
    if (data.qualityFlags && data.qualityFlags.length > 0) {
        const flagsList = document.getElementById('qualityFlagsList');
        flagsList.innerHTML = data.qualityFlags
            .map(flag => `<p>• ${flag}</p>`)
            .join('');
        document.getElementById('qualityFlagsSection').style.display = 'block';
    } else {
        document.getElementById('qualityFlagsSection').style.display = 'none';
    }

    // JSON Preview (pretty printed)
    const jsonPreview = document.getElementById('jsonPreview');
    jsonPreview.textContent = JSON.stringify(data, null, 2);

    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Reset form to initial state
 */
function resetForm() {
    issueKeyInput.value = '';
    issueKeyInput.focus();
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    currentResult = null;
}

/**
 * Download markdown file
 */
async function downloadMarkdown() {
    if (!currentResult) return;

    const issueKey = currentResult.issueKey;
    try {
        const response = await fetch(`/api/download/${issueKey}`);
        if (!response.ok) throw new Error('Download failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${issueKey}_test_plan.md`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        alert('Failed to download: ' + error.message);
    }
}

/**
 * Download JSON file
 */
async function downloadJSON() {
    if (!currentResult) return;

    const issueKey = currentResult.issueKey;
    try {
        const response = await fetch(`/api/download-json/${issueKey}`);
        if (!response.ok) throw new Error('Download failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${issueKey}_test_plan.json`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        alert('Failed to download: ' + error.message);
    }
}

/**
 * Copy JSON to clipboard
 */
async function copyJSON() {
    if (!currentResult) return;

    try {
        const jsonString = JSON.stringify(currentResult, null, 2);
        await navigator.clipboard.writeText(jsonString);

        // Show confirmation
        const button = document.getElementById('copyJSON');
        const originalText = button.innerHTML;
        button.innerHTML = '<span>✅</span> Copied!';
        setTimeout(() => {
            button.innerHTML = originalText;
        }, 2000);
    } catch (error) {
        alert('Failed to copy: ' + error.message);
    }
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    issueKeyInput.focus();
});
