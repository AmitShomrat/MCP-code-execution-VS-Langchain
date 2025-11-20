/**
 * MCP Benchmark Dashboard - Main Application Logic
 * 
 * Handles:
 * - User interactions
 * - API calls to backend
 * - UI updates
 * - Results display
 */

// Define API base URL for all endpoint calls
const API_BASE = '';

// Store current query results for comparison
let currentQueryResults = {
    query: '',
    traditional: null,
    codeExecution: null
};

// Cache DOM elements for main controls
const elements = {
    queryInput: document.getElementById('queryInput'),
    btnTraditional: document.getElementById('btnTraditional'),
    btnCodeExecution: document.getElementById('btnCodeExecution'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    loadingText: document.getElementById('loadingText')
};

// Cache DOM elements for Traditional MCP results display
const traditionalElements = {
    status: document.getElementById('traditionalStatus'),
    time: document.getElementById('traditionalTime'),
    calls: document.getElementById('traditionalCalls'),
    tokens: document.getElementById('traditionalTokens'),
    promptTokens: document.getElementById('traditionalPromptTokens'),
    completionTokens: document.getElementById('traditionalCompletionTokens'),
    output: document.getElementById('traditionalOutput')
};

// Cache DOM elements for Code Execution MCP results display
const codeExecElements = {
    status: document.getElementById('codeExecStatus'),
    time: document.getElementById('codeExecTime'),
    calls: document.getElementById('codeExecCalls'),
    tokens: document.getElementById('codeExecTokens'),
    promptTokens: document.getElementById('codeExecPromptTokens'),
    completionTokens: document.getElementById('codeExecCompletionTokens'),
    output: document.getElementById('codeExecOutput')
};

/**
 * Initialize event listeners for user interactions
 */
function initializeEventListeners() {
    // Attach click handler for Traditional MCP button
    elements.btnTraditional.addEventListener('click', () => runBenchmark('traditional'));
    
    // Attach click handler for Code Execution MCP button
    elements.btnCodeExecution.addEventListener('click', () => runBenchmark('code-execution'));
}

/**
 * Show loading overlay with custom message
 * @param {string} message - Loading message to display
 */
function showLoading(message = 'Processing...') {
    // Set loading text
    elements.loadingText.textContent = message;
    
    // Show overlay by adding active class
    elements.loadingOverlay.classList.add('active');
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    // Hide overlay by removing active class
    elements.loadingOverlay.classList.remove('active');
}

/**
 * Disable all action buttons during benchmark execution
 */
function disableButtons() {
    // Disable Traditional MCP button
    elements.btnTraditional.disabled = true;
    
    // Disable Code Execution MCP button
    elements.btnCodeExecution.disabled = true;
}

/**
 * Enable all action buttons after benchmark completion
 */
function enableButtons() {
    // Enable Traditional MCP button
    elements.btnTraditional.disabled = false;
    
    // Enable Code Execution MCP button
    elements.btnCodeExecution.disabled = false;
}

/**
 * Update status badge with new status and styling
 * @param {HTMLElement} statusElement - Status badge element
 * @param {string} status - Status text
 * @param {string} className - CSS class for styling
 */
function updateStatus(statusElement, status, className) {
    // Set status text
    statusElement.textContent = status;
    
    // Apply CSS class for styling
    statusElement.className = `status-badge ${className}`;
}

/**
 * Reset result display to initial state
 * @param {object} uiElements - UI elements object for specific approach
 */
function resetResultDisplay(uiElements) {
    // Reset all metric displays to placeholder
    uiElements.time.textContent = '--';
    uiElements.calls.textContent = '--';
    uiElements.tokens.textContent = '--';
    uiElements.promptTokens.textContent = '--';
    uiElements.completionTokens.textContent = '--';
    
    // Reset output display
    uiElements.output.textContent = 'Waiting for execution...';
}

/**
 * Display benchmark result in UI
 * @param {object} result - Benchmark result data
 * @param {object} uiElements - UI elements object for specific approach
 */
function displayResult(result, uiElements) {
    // Extract benchmark data from result
    const benchmark = result.result;
    
    // Animate execution time (with 's' suffix)
    animateNumber(uiElements.time, benchmark.time, 1200, 's');
    
    // Animate number of LLM calls
    animateNumber(uiElements.calls, benchmark.llm_calls.length, 800);
    
    // Animate total tokens used
    animateNumber(uiElements.tokens, benchmark.total_tokens.total_tokens, 1500);
    
    // Animate prompt tokens
    animateNumber(uiElements.promptTokens, benchmark.total_tokens.prompt_tokens, 1000);
    
    // Animate completion tokens
    animateNumber(uiElements.completionTokens, benchmark.total_tokens.completion_tokens, 1000);
    
    // Display final output or fallback
    uiElements.output.textContent = benchmark.final_output || 'No output';
    
    // Update status based on success
    if (benchmark.success) {
        updateStatus(uiElements.status, 'Complete', 'complete');
    } else {
        updateStatus(uiElements.status, 'Error', 'error');
        uiElements.output.textContent = benchmark.error || 'Execution failed';
    }
}

/**
 * Run benchmark for specified approach
 * @param {string} approach - 'traditional' or 'code-execution'
 */
async function runBenchmark(approach) {
    // Get query text from input
    const query = elements.queryInput.value.trim();
    
    // Validate query is not empty
    if (!query) {
        alert('Please enter a query');
        return;
    }
    
    // Store current query
    currentQueryResults.query = query;
    
    // Determine which approach is being run
    const isTraditional = approach === 'traditional';
    const uiElements = isTraditional ? traditionalElements : codeExecElements;
    const approachName = isTraditional ? 'Traditional MCP' : 'Code Execution MCP';
    
    // Map approach to endpoint name
    const endpointMap = {
        'traditional': 'traditional-mcp',
        'code-execution': 'code-execution-mcp'
    };
    const endpoint = `${API_BASE}/${endpointMap[approach]}`;
    
    try {
        // Disable buttons and show loading
        disableButtons();
        showLoading(`Running ${approachName} benchmark...`);
        
        // Update status to running
        updateStatus(uiElements.status, 'Running...', 'running');
        resetResultDisplay(uiElements);
        
        // Make API call to run benchmark
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        // Check if response is successful
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Benchmark failed');
        }
        
        // Parse response JSON
        const result = await response.json();
        
        // Store result for comparison
        if (isTraditional) {
            currentQueryResults.traditional = result.result;
        } else {
            currentQueryResults.codeExecution = result.result;
        }
        
        // Display results in UI
        displayResult(result, uiElements);
        
        // Show the specific result card that was executed
        const cardId = isTraditional ? 'traditionalResult' : 'codeExecResult';
        document.getElementById(cardId).classList.add('visible');
        
        // Show results section with animation
        document.querySelector('.results-section').classList.add('visible');
        
        // Log result to console
        console.log(`${approachName} Result:`, result);
        
        // Update comparison if both results available
        if (currentQueryResults.traditional && currentQueryResults.codeExecution) {
            updateCurrentComparison();
        }
        
    } catch (error) {
        // Handle errors
        console.error(`${approachName} Error:`, error);
        updateStatus(uiElements.status, 'Error', 'error');
        uiElements.output.textContent = `Error: ${error.message}`;
        alert(`Error running ${approachName}: ${error.message}`);
    } finally {
        // Always hide loading and enable buttons
        hideLoading();
        enableButtons();
    }
}

/**
 * Update comparison section with current query results
 */
function updateCurrentComparison() {
    // Show comparison section with animation
    document.querySelector('.comparison-section').classList.add('visible');
    
    // Update comparison table with current results
    displayCurrentComparisonTable();
    
    // Update comparison chart with current results
    updateCurrentComparisonChart();
    
    // Compare and highlight the winner
    compareAndHighlightWinner();
}

/**
 * Animate number from 0 to target value with easing
 * @param {HTMLElement} element - Element to update
 * @param {number} target - Target number
 * @param {number} duration - Animation duration in milliseconds
 * @param {string} suffix - Optional suffix (e.g., 's', 'ms')
 */
function animateNumber(element, target, duration = 1000, suffix = '') {
    // Parse target if it's a string
    const targetValue = typeof target === 'string' ? parseFloat(target) : target;
    
    // Skip animation if target is invalid
    if (isNaN(targetValue)) {
        element.textContent = target + suffix;
        return;
    }
    
    // Animation start time
    const startTime = performance.now();
    const startValue = 0;
    
    // Easing function (ease-out cubic)
    const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
    
    // Animation frame function
    function animate(currentTime) {
        // Calculate progress (0 to 1)
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Apply easing
        const easedProgress = easeOutCubic(progress);
        
        // Calculate current value
        const currentValue = startValue + (targetValue - startValue) * easedProgress;
        
        // Update element text with proper formatting
        if (targetValue % 1 === 0) {
            // Integer display
            element.textContent = Math.floor(currentValue) + suffix;
        } else {
            // Decimal display (preserve original decimal places)
            const decimalPlaces = target.toString().split('.')[1]?.length || 2;
            element.textContent = currentValue.toFixed(decimalPlaces) + suffix;
        }
        
        // Continue animation if not complete
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    // Start animation
    requestAnimationFrame(animate);
}

/**
 * Compare both benchmark results and highlight the winner
 */
function compareAndHighlightWinner() {
    // Get both result objects
    const traditional = currentQueryResults.traditional;
    const codeExec = currentQueryResults.codeExecution;
    
    // Exit if both results aren't available
    if (!traditional || !codeExec) {
        return;
    }
    
    // Get card elements
    const traditionalCard = document.getElementById('traditionalResult');
    const codeExecCard = document.getElementById('codeExecResult');
    
    // Remove existing winner classes
    traditionalCard.classList.remove('winner', 'loser');
    codeExecCard.classList.remove('winner', 'loser');
    
    // Remove existing improvement stats
    const existingStats = document.querySelectorAll('.improvement-stats');
    existingStats.forEach(stats => stats.remove());
    
    // Compare execution times
    const traditionalTime = traditional.time;
    const codeExecTime = codeExec.time;
    
    // Calculate time difference and percentage
    const timeDiff = Math.abs(traditionalTime - codeExecTime);
    const timePercentDiff = ((timeDiff / Math.max(traditionalTime, codeExecTime)) * 100).toFixed(1);
    
    // Compare token usage
    const traditionalTokens = extractTotalTokens(traditional);
    const codeExecTokens = extractTotalTokens(codeExec);
    
    // Calculate token difference and percentage
    const tokenDiff = Math.abs(traditionalTokens - codeExecTokens);
    const tokenPercentDiff = ((tokenDiff / Math.max(traditionalTokens, codeExecTokens)) * 100).toFixed(1);
    
    // Normalize scores (0-1 range) for fair comparison
    const maxTime = Math.max(traditionalTime, codeExecTime);
    const maxTokens = Math.max(traditionalTokens, codeExecTokens);
    
    // Calculate normalized scores (lower is better)
    const traditionalTimeScore = traditionalTime / maxTime;
    const codeExecTimeScore = codeExecTime / maxTime;
    const traditionalTokenScore = traditionalTokens / maxTokens;
    const codeExecTokenScore = codeExecTokens / maxTokens;
    
    // Calculate combined scores with equal weighting (50% time + 50% tokens)
    const traditionalCombinedScore = (traditionalTimeScore * 0.5) + (traditionalTokenScore * 0.5);
    const codeExecCombinedScore = (codeExecTimeScore * 0.5) + (codeExecTokenScore * 0.5);
    
    // Determine overall winner based on combined score (lower is better)
    const overallWinner = traditionalCombinedScore < codeExecCombinedScore ? 'traditional' : 'codeExec';
    const winnerCard = overallWinner === 'traditional' ? traditionalCard : codeExecCard;
    const loserCard = overallWinner === 'traditional' ? codeExecCard : traditionalCard;
    
    // Determine which metrics the winner excels at
    const timeWinner = traditionalTime < codeExecTime ? 'traditional' : 'codeExec';
    const tokenWinner = traditionalTokens < codeExecTokens ? 'traditional' : 'codeExec';
    
    // Build improvement text based on winner's strengths
    let improvementText = '';
    
    if (timeWinner === overallWinner && tokenWinner === overallWinner) {
        // Winner is better in both metrics
        improvementText = `${timePercentDiff}% Faster & ${tokenPercentDiff}% Fewer Tokens`;
    } else if (timeWinner === overallWinner) {
        // Winner is faster but uses more tokens
        improvementText = `${timePercentDiff}% Faster`;
    } else if (tokenWinner === overallWinner) {
        // Winner uses fewer tokens but is slower
        improvementText = `${tokenPercentDiff}% Fewer Tokens`;
    } else {
        // Winner by combined score
        improvementText = `Better Overall Performance`;
    }
    
    // Add winner/loser classes
    winnerCard.classList.add('winner');
    loserCard.classList.add('loser');
    
    // Create improvement stats element (below title)
    const improvementStats = document.createElement('div');
    improvementStats.className = 'improvement-stats';
    improvementStats.innerHTML = `${improvementText}`;
    
    // Insert improvement stats after card header
    const cardHeader = winnerCard.querySelector('.card-header');
    cardHeader.insertAdjacentElement('afterend', improvementStats);
    
    // Log comparison results
    console.log('Benchmark Comparison:', {
        timeWinner,
        timeDifference: `${timePercentDiff}%`,
        tokenWinner,
        tokenDifference: `${tokenPercentDiff}%`,
        overallWinner
    });
}

/**
 * Display comparison table for current query only
 */
function displayCurrentComparisonTable() {
    // Get table body element
    const tbody = document.getElementById('comparisonTableBody');
    tbody.innerHTML = '';
    
    // Format timestamp
    const now = new Date();
    const formattedDate = now.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    // Add Traditional MCP row
    if (currentQueryResults.traditional) {
        const row1 = document.createElement('tr');
        row1.innerHTML = `
            <td>${truncateText(currentQueryResults.query, 50)}</td>
            <td>Traditional MCP</td>
            <td>${currentQueryResults.traditional.time.toFixed(2)}s</td>
            <td>${extractTotalTokens(currentQueryResults.traditional).toLocaleString()}</td>
            <td>${currentQueryResults.traditional.llm_calls?.length || 0}</td>
            <td>${currentQueryResults.traditional.success ? '✅' : '❌'}</td>
            <td>${formattedDate}</td>
        `;
        tbody.appendChild(row1);
    }
    
    // Add Code Execution MCP row
    if (currentQueryResults.codeExecution) {
        const row2 = document.createElement('tr');
        row2.innerHTML = `
            <td>${truncateText(currentQueryResults.query, 50)}</td>
            <td>Code Execution MCP</td>
            <td>${currentQueryResults.codeExecution.time.toFixed(2)}s</td>
            <td>${extractTotalTokens(currentQueryResults.codeExecution).toLocaleString()}</td>
            <td>${currentQueryResults.codeExecution.llm_calls?.length || 0}</td>
            <td>${currentQueryResults.codeExecution.success ? '✅' : '❌'}</td>
            <td>${formattedDate}</td>
        `;
        tbody.appendChild(row2);
    }
}

/**
 * Extract total tokens from result data handling different formats
 * @param {object} result - Result object containing token information
 * @returns {number} Total token count
 */
function extractTotalTokens(result) {
    // Check if tokens object exists
    if (result.tokens) {
        // Try total_tokens first (Code Execution MCP format)
        // Fall back to total (Traditional MCP format)
        return result.tokens.total_tokens || result.tokens.total || 0;
    }
    
    // Check if total_tokens exists at top level
    if (result.total_tokens) {
        return result.total_tokens.total_tokens || 0;
    }
    
    // Return 0 if no token data found
    return 0;
}

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, maxLength) {
    // Return original if within limit
    if (text.length <= maxLength) return text;
    
    // Truncate and add ellipsis
    return text.substring(0, maxLength) + '...';
}

/**
 * Initialize theme toggle functionality
 */
function initializeThemeToggle() {
    // Get theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    
    // Exit if button not found
    if (!themeToggle) {
        return;
    }
    
    // Load saved theme from localStorage or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    // Apply saved theme to document
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Add click event listener to toggle theme
    themeToggle.addEventListener('click', () => {
        // Get current theme
        const currentTheme = document.documentElement.getAttribute('data-theme');
        
        // Toggle between dark and light
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Apply new theme
        document.documentElement.setAttribute('data-theme', newTheme);
        
        // Save to localStorage for persistence
        localStorage.setItem('theme', newTheme);
        
        // Log theme change
        console.log(`Theme changed to: ${newTheme}`);
    });
}

/**
 * Export current benchmark results as CSV
 */
function exportResultsAsCSV() {
    // Check if both results are available
    if (!currentQueryResults.traditional || !currentQueryResults.codeExecution) {
        alert('Please run both benchmarks before exporting');
        return;
    }
    
    // Get current timestamp for filename
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    
    // Prepare CSV data with headers
    const csvData = [
        ['Metric', 'Traditional MCP', 'Code Execution MCP', 'Difference'],
        ['Query', currentQueryResults.query, currentQueryResults.query, '-'],
        [
            'Execution Time (s)',
            currentQueryResults.traditional.time,
            currentQueryResults.codeExecution.time,
            (currentQueryResults.traditional.time - currentQueryResults.codeExecution.time).toFixed(2)
        ],
        [
            'LLM Calls',
            currentQueryResults.traditional.llm_calls.length,
            currentQueryResults.codeExecution.llm_calls.length,
            currentQueryResults.traditional.llm_calls.length - currentQueryResults.codeExecution.llm_calls.length
        ],
        [
            'Total Tokens',
            extractTotalTokens(currentQueryResults.traditional),
            extractTotalTokens(currentQueryResults.codeExecution),
            extractTotalTokens(currentQueryResults.traditional) - extractTotalTokens(currentQueryResults.codeExecution)
        ],
        [
            'Prompt Tokens',
            currentQueryResults.traditional.total_tokens.prompt_tokens,
            currentQueryResults.codeExecution.total_tokens.prompt_tokens,
            currentQueryResults.traditional.total_tokens.prompt_tokens - currentQueryResults.codeExecution.total_tokens.prompt_tokens
        ],
        [
            'Completion Tokens',
            currentQueryResults.traditional.total_tokens.completion_tokens,
            currentQueryResults.codeExecution.total_tokens.completion_tokens,
            currentQueryResults.traditional.total_tokens.completion_tokens - currentQueryResults.codeExecution.total_tokens.completion_tokens
        ],
        ['Success', currentQueryResults.traditional.success, currentQueryResults.codeExecution.success, '-']
    ];
    
    // Convert array to CSV string
    const csvContent = csvData.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
    
    // Create blob from CSV content
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    
    // Create download link
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    // Set link attributes
    link.setAttribute('href', url);
    link.setAttribute('download', `mcp-benchmark-comparison-${timestamp}.csv`);
    link.style.visibility = 'hidden';
    
    // Trigger download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Log export action
    console.log('Results exported as CSV');
}

/**
 * Initialize export button functionality
 */
function initializeExportButton() {
    // Get export button
    const exportBtn = document.getElementById('exportBtn');
    
    // Exit if button not found
    if (!exportBtn) {
        return;
    }
    
    // Add click event listener to export results
    exportBtn.addEventListener('click', exportResultsAsCSV);
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Set up event listeners
    initializeEventListeners();
    
    // Initialize export button
    initializeExportButton();
});
