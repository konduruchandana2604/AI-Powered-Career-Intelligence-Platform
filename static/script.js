"use strict";

/*
============================================================
AI POWERED CAREER INTELLIGENCE PLATFORM
Frontend Controller
============================================================
*/


// ============================================================
// APPLICATION STATE
// ============================================================

const AppState = {
    currentSection: "dashboardSection",
    currentAnalysis: null,
    selectedCareer: null,
    charts: {
        careerProbability: null,
        skillMatch: null,
        skillGap: null,
        modelComparison: null,
        analyticsModel: null
    },
    user: {
        name: "Demo User",
        email: "demo@example.com"
    }
};


// ============================================================
// DOM HELPERS
// ============================================================

function $(selector) {
    return document.querySelector(selector);
}


function $$(selector) {
    return Array.from(
        document.querySelectorAll(selector)
    );
}


function showElement(element) {
    if (!element) return;

    element.classList.remove("hidden");
}


function hideElement(element) {
    if (!element) return;

    element.classList.add("hidden");
}


function escapeHTML(value) {
    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function clamp(value, minimum = 0, maximum = 100) {
    const number = Number(value);

    if (!Number.isFinite(number)) {
        return minimum;
    }

    return Math.min(
        maximum,
        Math.max(
            minimum,
            number
        )
    );
}


function formatPercent(value) {
    if (
        value === null ||
        value === undefined ||
        !Number.isFinite(Number(value))
    ) {
        return "—";
    }

    return `${Number(value).toFixed(2)}%`;
}


function formatDate(dateString) {
    if (!dateString) {
        return "—";
    }

    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) {
        return dateString;
    }

    return date.toLocaleDateString(
        undefined,
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );
}


function formatDateTime(dateString) {
    if (!dateString) {
        return "—";
    }

    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) {
        return dateString;
    }

    return date.toLocaleString(
        undefined,
        {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}


// ============================================================
// TOAST NOTIFICATIONS
// ============================================================

function showToast(
    message,
    type = "info"
) {
    const container = $(
        "#toastContainer"
    );

    if (!container) return;

    const toast = document.createElement(
        "div"
    );

    toast.className = `toast toast-${type}`;

    const iconMap = {
        success: "✓",
        error: "!",
        warning: "!",
        info: "i"
    };

    toast.innerHTML = `
        <div class="toast-icon">
            ${iconMap[type] || "i"}
        </div>

        <div class="toast-message">
            ${escapeHTML(message)}
        </div>

        <button
            type="button"
            class="toast-close"
            aria-label="Close notification"
        >
            ×
        </button>
    `;

    container.appendChild(toast);

    const closeButton = toast.querySelector(
        ".toast-close"
    );

    closeButton.addEventListener(
        "click",
        () => {
            removeToast(toast);
        }
    );

    window.setTimeout(
        () => {
            removeToast(toast);
        },
        4500
    );
}


function removeToast(toast) {
    if (!toast) return;

    toast.classList.add(
        "toast-removing"
    );

    window.setTimeout(
        () => {
            toast.remove();
        },
        250
    );
}


// ============================================================
// LOADING STATE
// ============================================================

function setLoading(isLoading) {
    const overlay = $(
        "#loadingOverlay"
    );

    const analyzeButton = $(
        "#analyzeButton"
    );

    if (isLoading) {
        showElement(overlay);

        if (analyzeButton) {
            analyzeButton.disabled = true;

            analyzeButton.dataset.originalText =
                analyzeButton.innerHTML;

            analyzeButton.innerHTML = `
                <span class="button-spinner"></span>
                Analyzing...
            `;
        }
    } else {
        hideElement(overlay);

        if (analyzeButton) {
            analyzeButton.disabled = false;

            analyzeButton.innerHTML =
                analyzeButton.dataset.originalText ||
                "Analyze Resume <span>→</span>";
        }
    }
}


// ============================================================
// LOGIN
// ============================================================

function isLoggedIn() {
    return (
        sessionStorage.getItem(
            "career_ai_logged_in"
        ) === "true"
    );
}


function saveLoginState(user) {
    sessionStorage.setItem(
        "career_ai_logged_in",
        "true"
    );

    sessionStorage.setItem(
        "career_ai_user",
        JSON.stringify(user)
    );
}


function getStoredUser() {
    try {
        const stored = sessionStorage.getItem(
            "career_ai_user"
        );

        return stored
            ? JSON.parse(stored)
            : {
                name: "Demo User",
                email: "demo@example.com"
            };
    } catch {
        return {
            name: "Demo User",
            email: "demo@example.com"
        };
    }
}


function clearLoginState() {
    sessionStorage.removeItem(
        "career_ai_logged_in"
    );

    sessionStorage.removeItem(
        "career_ai_user"
    );
}


async function handleLogin(event) {
    event.preventDefault();

    const emailInput = $(
        "#loginEmail"
    );

    const passwordInput = $(
        "#loginPassword"
    );

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!email) {
        showToast(
            "Please enter your email.",
            "warning"
        );

        emailInput.focus();
        return;
    }

    if (!password) {
        showToast(
            "Please enter your password.",
            "warning"
        );

        passwordInput.focus();
        return;
    }

    const loginButton = $(
        "#loginButton"
    );

    loginButton.disabled = true;

    try {
        const response = await fetch(
            "/login",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(
                data.message ||
                "Login failed."
            );
        }

        const user = data.user || {
            name: "Demo User",
            email
        };

        saveLoginState(user);

        AppState.user = user;

        showApplication();

        showToast(
            "Login successful. Welcome back!",
            "success"
        );

    } catch (error) {
        showToast(
            error.message ||
            "Unable to log in.",
            "error"
        );
    } finally {
        loginButton.disabled = false;
    }
}


function showApplication() {
    hideElement(
        $("#loginScreen")
    );

    showElement(
        $("#appShell")
    );

    updateUserUI();

    loadHistory();

    updateProfile();

    checkModelStatus();

    navigateTo(
        "dashboardSection"
    );
}


function showLogin() {
    showElement(
        $("#loginScreen")
    );

    hideElement(
        $("#appShell")
    );
}


async function handleLogout() {
    try {
        await fetch(
            "/logout",
            {
                method: "POST"
            }
        );
    } catch {
        // Client-side state is still cleared below.
    }

    clearLoginState();

    AppState.currentAnalysis = null;
    AppState.selectedCareer = null;

    showLogin();

    showToast(
        "You have been logged out.",
        "success"
    );
}


function fillDemoCredentials() {
    $("#loginEmail").value =
        "demo@example.com";

    $("#loginPassword").value =
        "demo123";

    $("#loginPassword").type =
        "password";
}


// ============================================================
// PASSWORD VISIBILITY
// ============================================================

function togglePassword() {
    const input = $(
        "#loginPassword"
    );

    const button = $(
        "#togglePassword"
    );

    if (!input || !button) return;

    if (input.type === "password") {
        input.type = "text";
        button.textContent = "Hide";
    } else {
        input.type = "password";
        button.textContent = "Show";
    }
}


// ============================================================
// USER UI
// ============================================================

function updateUserUI() {
    const user = AppState.user;

    const firstName =
        user.name
            ? user.name.split(" ")[0]
            : "User";

    $("#headerUserName").textContent =
        user.name || "Demo User";

    $("#headerUserEmail").textContent =
        user.email || "";

    $("#welcomeName").textContent =
        firstName;

    $("#profileName").textContent =
        user.name || "Demo User";

    $("#profileEmail").textContent =
        user.email || "";
}


// ============================================================
// NAVIGATION
// ============================================================

const sectionTitles = {
    dashboardSection: "Dashboard",
    analyzeSection: "Analyze Resume",
    predictionsSection: "Career Predictions",
    skillGapSection: "Skill Gap Analysis",
    analyticsSection: "Analytics",
    profileSection: "Profile"
};


function navigateTo(sectionId) {
    const section = $(
        `#${sectionId}`
    );

    if (!section) return;

    $$(".page-section").forEach(
        item => {
            item.classList.remove(
                "active-section"
            );
        }
    );

    section.classList.add(
        "active-section"
    );

    $$(".nav-item").forEach(
        item => {
            item.classList.toggle(
                "active",
                item.dataset.section === sectionId
            );
        }
    );

    AppState.currentSection =
        sectionId;

    $("#headerTitle").textContent =
        sectionTitles[sectionId] ||
        "Career Intelligence";

    const sidebar = $(
        "#sidebar"
    );

    if (sidebar) {
        sidebar.classList.remove(
            "mobile-open"
        );
    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    if (
        sectionId ===
        "analyticsSection"
    ) {
        setTimeout(
            renderAllCharts,
            100
        );
    }

    if (
        sectionId ===
        "profileSection"
    ) {
        updateProfile();
    }
}


function setupNavigation() {
    $$(".nav-item").forEach(
        item => {
            item.addEventListener(
                "click",
                () => {
                    navigateTo(
                        item.dataset.section
                    );
                }
            );
        }
    );

    $$("[data-section]").forEach(
        element => {
            if (
                element.classList.contains(
                    "nav-item"
                )
            ) {
                return;
            }

            element.addEventListener(
                "click",
                () => {
                    const section =
                        element.dataset.section;

                    if (section) {
                        navigateTo(section);
                    }
                }
            );
        }
    );
}


function setupMobileMenu() {
    const button = $(
        "#mobileMenuButton"
    );

    const sidebar = $(
        "#sidebar"
    );

    if (!button || !sidebar) {
        return;
    }

    button.addEventListener(
        "click",
        () => {
            sidebar.classList.toggle(
                "mobile-open"
            );
        }
    );
}


// ============================================================
// FILE UPLOAD
// ============================================================

function setupFileUpload() {
    const fileInput = $(
        "#resumeFile"
    );

    const browseButton = $(
        "#browseButton"
    );

    const dropZone = $(
        "#dropZone"
    );

    if (!fileInput || !browseButton) {
        return;
    }

    browseButton.addEventListener(
        "click",
        () => {
            fileInput.click();
        }
    );

    fileInput.addEventListener(
        "change",
        () => {
            if (
                fileInput.files &&
                fileInput.files.length > 0
            ) {
                handleSelectedFile(
                    fileInput.files[0]
                );
            }
        }
    );

    if (dropZone) {
        [
            "dragenter",
            "dragover"
        ].forEach(
            eventName => {
                dropZone.addEventListener(
                    eventName,
                    event => {
                        event.preventDefault();

                        dropZone.classList.add(
                            "dragging"
                        );
                    }
                );
            }
        );

        [
            "dragleave",
            "drop"
        ].forEach(
            eventName => {
                dropZone.addEventListener(
                    eventName,
                    event => {
                        event.preventDefault();

                        dropZone.classList.remove(
                            "dragging"
                        );
                    }
                );
            }
        );

        dropZone.addEventListener(
            "drop",
            event => {
                const files =
                    event.dataTransfer.files;

                if (
                    files &&
                    files.length > 0
                ) {
                    handleSelectedFile(
                        files[0]
                    );

                    fileInput.files =
                        files;
                }
            }
        );
    }
}


function handleSelectedFile(file) {
    const extension =
        file.name
            .split(".")
            .pop()
            .toLowerCase();

    const allowed = [
        "pdf",
        "docx",
        "txt"
    ];

    if (!allowed.includes(extension)) {
        showToast(
            "Please upload a PDF, DOCX or TXT file.",
            "error"
        );

        return;
    }

    const maxSize =
        10 * 1024 * 1024;

    if (file.size > maxSize) {
        showToast(
            "File is larger than the 10 MB limit.",
            "error"
        );

        return;
    }

    $("#fileName").textContent =
        file.name;

    $("#fileMeta").textContent =
        `${extension.toUpperCase()} · ${formatFileSize(file.size)}`;

    hideElement(
        $("#dropZone")
    );

    showElement(
        $("#filePreview")
    );

    showToast(
        "Resume selected successfully.",
        "success"
    );
}


function formatFileSize(bytes) {
    if (bytes === 0) {
        return "0 Bytes";
    }

    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];

    const index = Math.floor(
        Math.log(bytes) /
        Math.log(1024)
    );

    return (
        `${(bytes / Math.pow(1024, index)).toFixed(2)} ` +
        `${units[index]}`
    );
}


function removeSelectedFile() {
    const fileInput = $(
        "#resumeFile"
    );

    fileInput.value = "";

    hideElement(
        $("#filePreview")
    );

    showElement(
        $("#dropZone")
    );
}


// ============================================================
// TEXT AREA
// ============================================================

function setupTextArea() {
    const textarea = $(
        "#resumeText"
    );

    const count = $(
        "#characterCount"
    );

    if (!textarea || !count) {
        return;
    }

    textarea.addEventListener(
        "input",
        () => {
            count.textContent =
                `${textarea.value.length.toLocaleString()} characters`;
        }
    );
}


// ============================================================
// ANALYZE
// ============================================================

function getAnalysisInput() {
    const fileInput = $(
        "#resumeFile"
    );

    const textarea = $(
        "#resumeText"
    );

    const hasFile =
        fileInput &&
        fileInput.files &&
        fileInput.files.length > 0;

    const hasText =
        textarea &&
        textarea.value.trim().length > 0;

    if (!hasFile && !hasText) {
        return null;
    }

    const formData =
        new FormData();

    if (hasFile) {
        formData.append(
            "resume",
            fileInput.files[0]
        );
    }

    if (hasText) {
        formData.append(
            "resume_text",
            textarea.value.trim()
        );
    }

    return formData;
}


async function analyzeResume() {
    const errorBox = $(
        "#analysisError"
    );

    hideElement(
        errorBox
    );

    const formData =
        getAnalysisInput();

    if (!formData) {
        const message =
            "Please upload a resume or enter your skills before analyzing.";

        showElement(
            errorBox
        );

        errorBox.textContent =
            message;

        showToast(
            message,
            "warning"
        );

        return;
    }

    setLoading(true);

    try {
        const response =
            await fetch(
                "/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );

        let data;

        try {
            data = await response.json();
        } catch {
            throw new Error(
                "The server returned an invalid response."
            );
        }

        if (
            !response.ok ||
            !data.success
        ) {
            throw new Error(
                data.message ||
                "Resume analysis failed."
            );
        }

        AppState.currentAnalysis =
            data;

        AppState.selectedCareer =
            data.top_career.name;

        saveAnalysisHistory(
            data
        );

        renderAnalysis(
            data
        );

        navigateTo(
            "dashboardSection"
        );

        showToast(
            "Career analysis completed successfully.",
            "success"
        );

    } catch (error) {
        console.error(error);

        showElement(
            errorBox
        );

        errorBox.textContent =
            error.message ||
            "Unable to analyze your resume.";

        showToast(
            error.message ||
            "Unable to analyze your resume.",
            "error"
        );

    } finally {
        setLoading(false);
    }
}


// ============================================================
// RENDER COMPLETE ANALYSIS
// ============================================================

function renderAnalysis(data) {
    if (
        !data ||
        !data.top_career
    ) {
        return;
    }

    renderTopCareer(
        data
    );

    renderPredictions(
        data
    );

    renderSkillGap(
        data
    );

    renderModelComparison(
        data
    );

    renderDashboardSkills(
        data
    );

    renderDashboardPredictions(
        data
    );

    renderAllCharts();

    updateProfile();
}


// ============================================================
// TOP CAREER
// ============================================================

function renderTopCareer(data) {
    const top =
        data.top_career;

    $("#dashboardTopCareer").textContent =
        top.name;

    $("#dashboardConfidence").textContent =
        formatPercent(
            top.confidence
        );

    $("#dashboardMatched").textContent =
        top.matched_count ?? 0;

    $("#dashboardMissing").textContent =
        top.missing_count ?? 0;

    $("#topCareerName").textContent =
        top.name;

    $("#topCareerDescription").textContent =
        top.description ||
        "Career recommendation generated from your profile.";

    $("#topCareerConfidence").textContent =
        formatPercent(
            top.confidence
        );

    $("#topCareerMatch").textContent =
        formatPercent(
            top.skill_match
        );

    $("#topCareerGap").textContent =
        formatPercent(
            top.skill_gap
        );

    $("#topCareerReadiness").textContent =
        top.readiness_score !== null &&
        top.readiness_score !== undefined
            ? `${top.readiness_score}/100`
            : "—";

    $("#readinessValue").textContent =
        top.readiness_score !== null &&
        top.readiness_score !== undefined
            ? `${top.readiness_score}%`
            : "—";

    const readinessCircle = $(
        ".readiness-circle"
    );

    if (
        readinessCircle &&
        top.readiness_score !== null
    ) {
        const score =
            clamp(
                top.readiness_score
            );

        readinessCircle.style.setProperty(
            "--readiness",
            `${score * 3.6}deg`
        );
    }
}


// ============================================================
// TOP 5 PREDICTIONS
// ============================================================

function renderPredictions(data) {
    const grid = $(
        "#predictionsGrid"
    );

    if (!grid) return;

    const predictions =
        data.predictions || [];

    if (!predictions.length) {
        grid.innerHTML = `
            <div class="empty-state full-width">
                <div class="empty-icon">◆</div>
                <h3>No predictions available</h3>
                <p>
                    The ML models did not return any career predictions.
                </p>
            </div>
        `;

        return;
    }

    grid.innerHTML =
        predictions
            .map(
                prediction =>
                    createCareerCard(
                        prediction
                    )
            )
            .join("");
}


function createCareerCard(prediction) {
    const rank =
        prediction.rank;

    const confidence =
        clamp(
            prediction.confidence
        );

    const match =
        clamp(
            prediction.skill_match
        );

    const rankClass =
        rank === 1
            ? "rank-first"
            : "";

    return `
        <article
            class="career-card ${rankClass}"
            data-career="${escapeHTML(prediction.career)}"
        >

            <div class="career-card-top">

                <div class="rank-badge">
                    #${rank}
                </div>

                <span class="prediction-label">
                    ML MATCH
                </span>

            </div>

            <h3>
                ${escapeHTML(prediction.career)}
            </h3>

            <div class="career-confidence">

                <strong>
                    ${confidence.toFixed(2)}%
                </strong>

                <span>
                    confidence
                </span>

            </div>

            <div class="progress-track">
                <div
                    class="progress-fill"
                    style="width: ${confidence}%"
                ></div>
            </div>

            <div class="career-card-stats">

                <span>
                    Skill Match
                </span>

                <strong>
                    ${match.toFixed(2)}%
                </strong>

            </div>

            <button
                type="button"
                class="btn btn-secondary btn-full career-details-button"
                data-career="${escapeHTML(prediction.career)}"
            >
                View Details
                <span>→</span>
            </button>

        </article>
    `;
}


function setupPredictionDelegation() {
    const grid = $(
        "#predictionsGrid"
    );

    if (!grid) return;

    grid.addEventListener(
        "click",
        event => {
            const button =
                event.target.closest(
                    ".career-details-button"
                );

            if (!button) {
                return;
            }

            const career =
                button.dataset.career;

            selectCareer(
                career
            );
        }
    );
}


async function selectCareer(career) {
    if (!career) return;

    AppState.selectedCareer =
        career;

    const data =
        AppState.currentAnalysis;

    if (!data) {
        showToast(
            "Analyze your resume first.",
            "warning"
        );

        return;
    }

    const candidateSkills =
        data.skills?.identified || [];

    navigateTo(
        "predictionsSection"
    );

    try {
        const response =
            await fetch(
                "/career-details",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify({
                        career,
                        candidate_skills:
                            candidateSkills
                    })
                }
            );

        const result =
            await response.json();

        if (
            !response.ok ||
            !result.success
        ) {
            throw new Error(
                result.message ||
                "Unable to load career details."
            );
        }

        renderCareerDetails(
            result
        );

    } catch (error) {
        showToast(
            error.message ||
            "Unable to load career details.",
            "error"
        );
    }
}


// ============================================================
// CAREER DETAILS
// ============================================================

function renderCareerDetails(data) {
    const panel = $(
        "#careerDetailPanel"
    );

    if (!panel) return;

    const gap =
        data.skill_gap || {};

    const matched =
        gap.matched_skills || [];

    const missing =
        gap.missing_skills || [];

    const recommendations =
        data.recommendations || [];

    panel.innerHTML = `
        <div class="career-detail-header">

            <div>

                <span class="section-eyebrow">
                    SELECTED CAREER
                </span>

                <h2>
                    ${escapeHTML(data.career)}
                </h2>

                <p>
                    Career-specific skill alignment
                    based on your submitted profile.
                </p>

            </div>

            <div class="detail-match-score">
                <strong>
                    ${formatPercent(gap.skill_match)}
                </strong>

                <span>
                    skill match
                </span>
            </div>

        </div>

        <div class="detail-columns">

            <div>

                <div class="detail-section-title">
                    <span class="success-symbol">✓</span>
                    Matched Skills
                </div>

                <div class="skill-badge-container">
                    ${
                        matched.length
                            ? matched.map(
                                skill =>
                                    `
                                    <span class="skill-badge matched">
                                        ✓ ${escapeHTML(skill)}
                                    </span>
                                    `
                            ).join("")
                            : `
                                <span class="muted-text">
                                    No matched skills found.
                                </span>
                            `
                    }
                </div>

            </div>

            <div>

                <div class="detail-section-title">
                    <span class="warning-symbol">+</span>
                    Missing Skills
                </div>

                <div class="skill-badge-container">
                    ${
                        missing.length
                            ? missing.map(
                                skill =>
                                    `
                                    <span class="skill-badge missing">
                                        + ${escapeHTML(skill)}
                                    </span>
                                    `
                            ).join("")
                            : `
                                <span class="muted-text">
                                    No skill gap detected.
                                </span>
                            `
                    }
                </div>

            </div>

        </div>

        <div class="detail-footer">

            <div>
                <span>
                    Required Skills
                </span>

                <strong>
                    ${gap.required_skills?.length || 0}
                </strong>
            </div>

            <div>
                <span>
                    Matched
                </span>

                <strong>
                    ${gap.matched_count || 0}
                </strong>
            </div>

            <div>
                <span>
                    Missing
                </span>

                <strong>
                    ${gap.missing_count || 0}
                </strong>
            </div>

            <div>
                <span>
                    Readiness
                </span>

                <strong>
                    ${
                        gap.readiness_score !== null &&
                        gap.readiness_score !== undefined
                            ? `${gap.readiness_score}/100`
                            : "—"
                    }
                </strong>
            </div>

        </div>

        ${
            recommendations.length
                ? `
                    <div class="career-detail-recommendations">

                        <div class="detail-section-title">
                            <span>✦</span>
                            Recommended Learning
                        </div>

                        ${recommendations
                            .slice(0, 4)
                            .map(
                                item =>
                                    `
                                    <div class="mini-recommendation">

                                        <strong>
                                            ${escapeHTML(item.skill)}
                                        </strong>

                                        <p>
                                            ${escapeHTML(item.recommendation)}
                                        </p>

                                    </div>
                                    `
                            )
                            .join("")}

                    </div>
                `
                : ""
        }
    `;
}


// ============================================================
// DASHBOARD PREDICTIONS
// ============================================================

function renderDashboardPredictions(data) {
    const container = $(
        "#dashboardPredictions"
    );

    if (!container) return;

    const predictions =
        data.predictions || [];

    if (!predictions.length) {
        container.innerHTML = `
            <div class="empty-state compact">
                <span>◆</span>
                <p>
                    Analyze your profile to see career predictions.
                </p>
            </div>
        `;

        return;
    }

    container.innerHTML =
        predictions
            .slice(0, 5)
            .map(
                item =>
                    `
                    <button
                        type="button"
                        class="mini-prediction"
                        data-career="${escapeHTML(item.career)}"
                    >

                        <span class="mini-rank">
                            #${item.rank}
                        </span>

                        <span class="mini-career">
                            ${escapeHTML(item.career)}
                        </span>

                        <span class="mini-confidence">
                            ${formatPercent(item.confidence)}
                        </span>

                    </button>
                    `
            )
            .join("");

    container
        .querySelectorAll(
            ".mini-prediction"
        )
        .forEach(
            button => {
                button.addEventListener(
                    "click",
                    () => {
                        selectCareer(
                            button.dataset.career
                        );
                    }
                );
            }
        );
}


// ============================================================
// SKILL GAP RENDERING
// ============================================================

function renderSkillGap(data) {
    const gap =
        data.skill_gap || {};

    $("#skillGapCareer").textContent =
        gap.career ||
        data.top_career?.name ||
        "—";

    $("#skillGapReadiness").textContent =
        gap.readiness_score !== null &&
        gap.readiness_score !== undefined
            ? gap.readiness_score
            : "—";

    $("#overallSkillMatch").textContent =
        formatPercent(
            gap.skill_match
        );

    $("#overallSkillGap").textContent =
        formatPercent(
            gap.skill_gap
        );

    const match =
        clamp(gap.skill_match);

    const gapValue =
        clamp(gap.skill_gap);

    $("#overallSkillMatchBar").style.width =
        `${match}%`;

    $("#overallSkillGapBar").style.width =
        `${gapValue}%`;

    const matched =
        gap.matched_skills || [];

    const missing =
        gap.missing_skills || [];

    $("#matchedSkillCount").textContent =
        matched.length;

    $("#missingSkillCount").textContent =
        missing.length;

    renderSkillList(
        "#matchedSkills",
        matched,
        "matched"
    );

    renderSkillList(
        "#missingSkills",
        missing,
        "missing"
    );

    renderPriority(
        gap.priority || {}
    );

    renderRecommendations(
        data.recommendations || []
    );
}


function renderSkillList(
    selector,
    skills,
    type
) {
    const container = $(
        selector
    );

    if (!container) return;

    if (!skills.length) {
        container.innerHTML = `
            <span class="muted-text">
                No ${type === "matched"
                    ? "matched"
                    : "missing"} skills.
            </span>
        `;

        return;
    }

    container.innerHTML =
        skills
            .map(
                skill =>
                    `
                    <span class="skill-badge ${type}">
                        ${
                            type === "matched"
                                ? "✓"
                                : "+"
                        }
                        ${escapeHTML(skill)}
                    </span>
                    `
            )
            .join("");
}


function renderPriority(priority) {
    renderPriorityList(
        "#highPrioritySkills",
        priority.high || []
    );

    renderPriorityList(
        "#mediumPrioritySkills",
        priority.medium || []
    );

    renderPriorityList(
        "#lowPrioritySkills",
        priority.low || []
    );
}


function renderPriorityList(
    selector,
    skills
) {
    const container = $(
        selector
    );

    if (!container) return;

    if (!skills.length) {
        container.innerHTML = `
            <span class="muted-text">
                None
            </span>
        `;

        return;
    }

    container.innerHTML =
        skills
            .map(
                skill =>
                    `
                    <span class="priority-skill">
                        ${escapeHTML(skill)}
                    </span>
                    `
            )
            .join("");
}


function renderRecommendations(
    recommendations
) {
    const container = $(
        "#recommendationsList"
    );

    if (!container) return;

    if (!recommendations.length) {
        container.innerHTML = `
            <div class="empty-state compact">
                <div class="empty-icon">
                    ✓
                </div>

                <p>
                    No additional skill recommendations
                    are required for the current profile.
                </p>
            </div>
        `;

        return;
    }

    container.innerHTML =
        recommendations
            .map(
                item =>
                    `
                    <article class="recommendation-card">

                        <div class="recommendation-icon">
                            ✦
                        </div>

                        <div class="recommendation-content">

                            <div class="recommendation-title">

                                <h4>
                                    ${escapeHTML(item.skill)}
                                </h4>

                                <span class="priority-label ${escapeHTML(item.priority)}">
                                    ${escapeHTML(item.priority)}
                                </span>

                            </div>

                            <p>
                                ${escapeHTML(item.recommendation)}
                            </p>

                        </div>

                    </article>
                    `
            )
            .join("");
}


// ============================================================
// DASHBOARD SKILLS
// ============================================================

function renderDashboardSkills(data) {
    const gap =
        data.skill_gap || {};

    const match =
        clamp(gap.skill_match);

    const missing =
        clamp(gap.skill_gap);

    $("#dashboardMatchPercent").textContent =
        `${match.toFixed(2)}%`;

    $("#dashboardGapPercent").textContent =
        `${missing.toFixed(2)}%`;

    $("#dashboardMatchBar").style.width =
        `${match}%`;

    $("#dashboardGapBar").style.width =
        `${missing}%`;

    const chips =
        $("#dashboardSkillChips");

    if (!chips) return;

    const skills =
        data.skills?.identified || [];

    if (!skills.length) {
        chips.innerHTML = `
            <span class="muted-text">
                No skills detected.
            </span>
        `;

        return;
    }

    chips.innerHTML =
        skills
            .slice(0, 12)
            .map(
                skill =>
                    `
                    <span class="skill-chip">
                        ${escapeHTML(skill)}
                    </span>
                    `
            )
            .join("");
}


// ============================================================
// MODEL COMPARISON
// ============================================================

function getModelDisplayName(name) {
    const names = {
        logistic_regression:
            "Logistic Regression",
        random_forest:
            "Random Forest",
        xgboost:
            "XGBoost"
    };

    return names[name] ||
        name;
}


function renderModelComparison(data) {
    const container = $(
        "#modelComparisonList"
    );

    if (!container) return;

    const models =
        data.models || {};

    const modelNames = [
        "logistic_regression",
        "random_forest",
        "xgboost"
    ];

    container.innerHTML =
        modelNames
            .map(
                name => {
                    const model =
                        models[name] || {};

                    const available =
                        model.available;

                    const confidence =
                        model.confidence;

                    return `
                        <div class="model-row">

                            <div class="model-row-name">

                                <span
                                    class="model-status-dot ${
                                        available
                                            ? "available"
                                            : "unavailable"
                                    }"
                                ></span>

                                <strong>
                                    ${getModelDisplayName(name)}
                                </strong>

                            </div>

                            <div class="model-career">
                                ${
                                    available
                                        ? escapeHTML(
                                            model.career || "—"
                                        )
                                        : "Unavailable"
                                }
                            </div>

                            <strong class="model-confidence">
                                ${
                                    available
                                        ? formatPercent(
                                            confidence
                                        )
                                        : "—"
                                }
                            </strong>

                        </div>
                    `;
                }
            )
            .join("");

    renderModelChart(
        models
    );
}


// ============================================================
// HISTORY
// ============================================================

function getHistory() {
    try {
        const stored =
            localStorage.getItem(
                "career_ai_history"
            );

        if (!stored) {
            return [];
        }

        const history =
            JSON.parse(stored);

        return Array.isArray(history)
            ? history
            : [];

    } catch {
        return [];
    }
}


function saveAnalysisHistory(data) {
    if (
        !data ||
        !data.top_career
    ) {
        return;
    }

    const history =
        getHistory();

    const entry = {
        id:
            `${Date.now()}_${Math.random()
                .toString(36)
                .slice(2)}`,

        timestamp:
            data.timestamp ||
            new Date().toISOString(),

        top_career:
            data.top_career.name,

        confidence:
            data.top_career.confidence,

        skill_match:
            data.top_career.skill_match,

        skill_gap:
            data.top_career.skill_gap,

        analysis:
            data
    };

    history.unshift(
        entry
    );

    // Keep browser storage lightweight.
    const limited =
        history.slice(0, 20);

    try {
        localStorage.setItem(
            "career_ai_history",
            JSON.stringify(limited)
        );
    } catch {
        // If storage is full, remove older records.
        try {
            localStorage.setItem(
                "career_ai_history",
                JSON.stringify(
                    limited.slice(0, 5)
                )
            );
        } catch {
            console.warn(
                "Unable to save analysis history."
            );
        }
    }

    renderHistory(
        limited
    );
}


function loadHistory() {
    renderHistory(
        getHistory()
    );
}


function renderHistory(history) {
    const tbody = $(
        "#historyTableBody"
    );

    if (!tbody) return;

    if (!history.length) {
        tbody.innerHTML = `
            <tr>
                <td
                    colspan="5"
                    class="table-empty"
                >
                    No previous analysis found.
                </td>
            </tr>
        `;

        return;
    }

    tbody.innerHTML =
        history
            .map(
                item =>
                    `
                    <tr>

                        <td>
                            ${escapeHTML(
                                formatDate(
                                    item.timestamp
                                )
                            )}
                        </td>

                        <td>
                            <strong>
                                ${escapeHTML(
                                    item.top_career
                                )}
                            </strong>
                        </td>

                        <td>
                            <span class="table-confidence">
                                ${formatPercent(
                                    item.confidence
                                )}
                            </span>
                        </td>

                        <td>
                            ${formatPercent(
                                item.skill_match
                            )}
                        </td>

                        <td>
                            <button
                                type="button"
                                class="table-action history-view-button"
                                data-history-id="${escapeHTML(item.id)}"
                            >
                                View
                            </button>
                        </td>

                    </tr>
                    `
            )
            .join("");

    tbody
        .querySelectorAll(
            ".history-view-button"
        )
        .forEach(
            button => {
                button.addEventListener(
                    "click",
                    () => {
                        loadHistoryEntry(
                            button.dataset.historyId
                        );
                    }
                );
            }
        );
}


function loadHistoryEntry(id) {
    const history =
        getHistory();

    const entry =
        history.find(
            item => item.id === id
        );

    if (!entry || !entry.analysis) {
        showToast(
            "Stored analysis could not be loaded.",
            "error"
        );

        return;
    }

    AppState.currentAnalysis =
        entry.analysis;

    AppState.selectedCareer =
        entry.analysis.top_career?.name ||
        null;

    renderAnalysis(
        entry.analysis
    );

    navigateTo(
        "dashboardSection"
    );

    showToast(
        "Previous analysis loaded.",
        "success"
    );
}


function clearHistory() {
    const history =
        getHistory();

    if (!history.length) {
        showToast(
            "There is no analysis history to clear.",
            "info"
        );

        return;
    }

    const confirmed =
        window.confirm(
            "Clear all saved analysis history?"
        );

    if (!confirmed) {
        return;
    }

    localStorage.removeItem(
        "career_ai_history"
    );

    renderHistory(
        []
    );

    updateProfile();

    showToast(
        "Analysis history cleared.",
        "success"
    );
}


// ============================================================
// PROFILE
// ============================================================

function updateProfile() {
    const history =
        getHistory();

    $("#profileAnalysisCount").textContent =
        history.length;

    if (!history.length) {
        $("#profileLatestCareer").textContent =
            "—";

        $("#profileLatestMatch").textContent =
            "—";

        $("#profileLatestDate").textContent =
            "—";

        return;
    }

    const latest =
        history[0];

    $("#profileLatestCareer").textContent =
        latest.top_career ||
        "—";

    $("#profileLatestMatch").textContent =
        formatPercent(
            latest.skill_match
        );

    $("#profileLatestDate").textContent =
        formatDateTime(
            latest.timestamp
        );
}


// ============================================================
// MODEL STATUS
// ============================================================

async function checkModelStatus() {
    const container = $(
        "#profileModelStatus"
    );

    try {
        const response =
            await fetch(
                "/api/model-status"
            );

        const data =
            await response.json();

        if (
            !response.ok ||
            !data.success
        ) {
            throw new Error(
                "Unable to retrieve model status."
            );
        }

        const models =
            data.models || {};

        const names = [
            "logistic_regression",
            "random_forest",
            "xgboost"
        ];

        container.innerHTML =
            names
                .map(
                    name => {
                        const model =
                            models[name] || {};

                        return `
                            <div class="system-status-card">

                                <div class="system-status-icon">
                                    ML
                                </div>

                                <div>

                                    <strong>
                                        ${getModelDisplayName(name)}
                                    </strong>

                                    <span class="${
                                        model.available
                                            ? "system-online"
                                            : "system-offline"
                                    }">

                                        <i></i>

                                        ${
                                            model.available
                                                ? "Available"
                                                : "Unavailable"
                                        }

                                    </span>

                                </div>

                            </div>
                        `;
                    }
                )
                .join("");

    } catch (error) {
        container.innerHTML = `
            <div class="alert alert-error">
                Unable to retrieve model status.
            </div>
        `;
    }
}


// ============================================================
// CHART HELPERS
// ============================================================

function destroyChart(
    chartKey
) {
    const chart =
        AppState.charts[chartKey];

    if (chart) {
        chart.destroy();

        AppState.charts[chartKey] =
            null;
    }
}


function chartHasCanvas(
    selector
) {
    return Boolean(
        $(selector)
    );
}


function renderCareerProbabilityChart() {
    if (
        !AppState.currentAnalysis ||
        !chartHasCanvas(
            "#careerProbabilityChart"
        )
    ) {
        return;
    }

    const predictions =
        AppState.currentAnalysis.predictions ||
        [];

    destroyChart(
        "careerProbability"
    );

    const context = $(
        "#careerProbabilityChart"
    ).getContext("2d");

    AppState.charts.careerProbability =
        new Chart(
            context,
            {
                type: "bar",

                data: {
                    labels:
                        predictions.map(
                            item =>
                                item.career
                        ),

                    datasets: [
                        {
                            label:
                                "Confidence (%)",

                            data:
                                predictions.map(
                                    item =>
                                        item.confidence
                                ),

                            borderWidth: 0,

                            borderRadius: 8
                        }
                    ]
                },

                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            display: false
                        },

                        tooltip: {
                            callbacks: {
                                label:
                                    context =>
                                        `${context.raw.toFixed(2)}% confidence`
                            }
                        }
                    },

                    scales: {
                        x: {
                            grid: {
                                display: false
                            }
                        },

                        y: {
                            beginAtZero: true,
                            max: 100,

                            ticks: {
                                callback:
                                    value =>
                                        `${value}%`
                            }
                        }
                    }
                }
            }
        );
}


function renderSkillMatchChart() {
    if (
        !AppState.currentAnalysis ||
        !chartHasCanvas(
            "#skillMatchChart"
        )
    ) {
        return;
    }

    const gap =
        AppState.currentAnalysis.skill_gap ||
        {};

    destroyChart(
        "skillMatch"
    );

    const context = $(
        "#skillMatchChart"
    ).getContext("2d");

    AppState.charts.skillMatch =
        new Chart(
            context,
            {
                type: "doughnut",

                data: {
                    labels: [
                        "Matched",
                        "Missing"
                    ],

                    datasets: [
                        {
                            data: [
                                gap.matched_count || 0,
                                gap.missing_count || 0
                            ],

                            borderWidth: 0
                        }
                    ]
                },

                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "68%",

                    plugins: {
                        legend: {
                            position: "bottom"
                        }
                    }
                }
            }
        );
}


function renderSkillGapChart() {
    if (
        !AppState.currentAnalysis ||
        !chartHasCanvas(
            "#skillGapChart"
        )
    ) {
        return;
    }

    const gap =
        AppState.currentAnalysis.skill_gap ||
        {};

    destroyChart(
        "skillGap"
    );

    const context = $(
        "#skillGapChart"
    ).getContext("2d");

    AppState.charts.skillGap =
        new Chart(
            context,
            {
                type: "doughnut",

                data: {
                    labels: [
                        "Skill Match",
                        "Skill Gap"
                    ],

                    datasets: [
                        {
                            data: [
                                gap.skill_match || 0,
                                gap.skill_gap || 0
                            ],

                            borderWidth: 0
                        }
                    ]
                },

                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "68%",

                    plugins: {
                        legend: {
                            position: "bottom"
                        }
                    }
                }
            }
        );
}


function renderModelChart(
    models
) {
    if (
        !chartHasCanvas(
            "#modelComparisonChart"
        )
    ) {
        return;
    }

    destroyChart(
        "modelComparison"
    );

    const names = [
        "logistic_regression",
        "random_forest",
        "xgboost"
    ];

    const values =
        names.map(
            name => {
                const model =
                    models[name] || {};

                return model.available
                    ? Number(
                        model.confidence || 0
                    )
                    : 0;
            }
        );

    const context = $(
        "#modelComparisonChart"
    ).getContext("2d");

    AppState.charts.modelComparison =
        new Chart(
            context,
            {
                type: "bar",

                data: {
                    labels:
                        names.map(
                            getModelDisplayName
                        ),

                    datasets: [
                        {
                            label:
                                "Confidence (%)",

                            data:
                                values,

                            borderRadius: 8,

                            borderWidth: 0
                        }
                    ]
                },

                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            display: false
                        }
                    },

                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,

                            ticks: {
                                callback:
                                    value =>
                                        `${value}%`
                            }
                        },

                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            }
        );
}


function renderAnalyticsModelChart() {
    if (
        !AppState.currentAnalysis ||
        !chartHasCanvas(
            "#analyticsModelChart"
        )
    ) {
        return;
    }

    const models =
        AppState.currentAnalysis.models ||
        {};

    destroyChart(
        "analyticsModel"
    );

    const names = [
        "logistic_regression",
        "random_forest",
        "xgboost"
    ];

    const values =
        names.map(
            name => {
                const model =
                    models[name] || {};

                return model.available
                    ? Number(
                        model.confidence || 0
                    )
                    : 0;
            }
        );

    const context = $(
        "#analyticsModelChart"
    ).getContext("2d");

    AppState.charts.analyticsModel =
        new Chart(
            context,
            {
                type: "bar",

                data: {
                    labels:
                        names.map(
                            getModelDisplayName
                        ),

                    datasets: [
                        {
                            label:
                                "Model Confidence (%)",

                            data:
                                values,

                            borderWidth: 0,

                            borderRadius: 8
                        }
                    ]
                },

                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        },

                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            }
        );
}


function renderAllCharts() {
    if (!AppState.currentAnalysis) {
        return;
    }

    renderCareerProbabilityChart();

    renderSkillMatchChart();

    renderSkillGapChart();

    renderAnalyticsModelChart();

    const models =
        AppState.currentAnalysis.models ||
        {};

    renderModelChart(
        models
    );
}


// ============================================================
// BUTTON EVENT SETUP
// ============================================================

function setupButtons() {
    const loginForm = $(
        "#loginForm"
    );

    if (loginForm) {
        loginForm.addEventListener(
            "submit",
            handleLogin
        );
    }

    const logoutButton = $(
        "#logoutButton"
    );

    if (logoutButton) {
        logoutButton.addEventListener(
            "click",
            handleLogout
        );
    }

    const toggleButton = $(
        "#togglePassword"
    );

    if (toggleButton) {
        toggleButton.addEventListener(
            "click",
            togglePassword
        );
    }

    const demoButton = $(
        "#fillDemoButton"
    );

    if (demoButton) {
        demoButton.addEventListener(
            "click",
            fillDemoCredentials
        );
    }

    const analyzeButton = $(
        "#analyzeButton"
    );

    if (analyzeButton) {
        analyzeButton.addEventListener(
            "click",
            analyzeResume
        );
    }

    const removeFileButton = $(
        "#removeFileButton"
    );

    if (removeFileButton) {
        removeFileButton.addEventListener(
            "click",
            removeSelectedFile
        );
    }

    const clearHistoryButton = $(
        "#clearHistoryButton"
    );

    if (clearHistoryButton) {
        clearHistoryButton.addEventListener(
            "click",
            clearHistory
        );
    }
}


// ============================================================
// SESSION INITIALIZATION
// ============================================================

function initializeApplication() {
    AppState.user =
        getStoredUser();

    setupButtons();

    setupNavigation();

    setupMobileMenu();

    setupFileUpload();

    setupTextArea();

    setupPredictionDelegation();

    if (isLoggedIn()) {
        showApplication();
    } else {
        showLogin();
    }
}


// ============================================================
// DOM READY
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    initializeApplication
);