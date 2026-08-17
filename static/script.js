document.addEventListener(
    "DOMContentLoaded",
    function () {


        // =====================================================
        // ELEMENTS
        // =====================================================

        const form =
            document.getElementById(
                "resumeForm"
            );

        const fileInput =
            document.getElementById(
                "resume"
            );

        const chooseFile =
            document.getElementById(
                "chooseFile"
            );

        const uploadBox =
            document.getElementById(
                "uploadBox"
            );

        const selectedFile =
            document.getElementById(
                "selectedFile"
            );

        const analyzeButton =
            document.getElementById(
                "analyzeButton"
            );

        const buttonText =
            document.getElementById(
                "buttonText"
            );

        const loader =
            document.getElementById(
                "loader"
            );

        const errorBox =
            document.getElementById(
                "errorBox"
            );

        const errorMessage =
            document.getElementById(
                "errorMessage"
            );

        const results =
            document.getElementById(
                "results"
            );

        const resetButton =
            document.getElementById(
                "resetButton"
            );


        // =====================================================
        // CHOOSE FILE
        // =====================================================

        chooseFile.addEventListener(
            "click",
            function () {

                fileInput.click();

            }
        );


        // =====================================================
        // FILE SELECTED
        // =====================================================

        fileInput.addEventListener(
            "change",
            function () {

                showSelectedFile();

            }
        );


        function showSelectedFile() {

            if (
                !fileInput.files ||
                fileInput.files.length === 0
            ) {

                selectedFile.textContent =
                    "";

                return;
            }


            const file =
                fileInput.files[0];


            const allowedTypes = [
                "pdf",
                "docx",
                "txt"
            ];


            const extension =
                file.name
                    .split(".")
                    .pop()
                    .toLowerCase();


            if (
                !allowedTypes.includes(
                    extension
                )
            ) {

                selectedFile.textContent =
                    "Please select PDF, DOCX or TXT.";

                fileInput.value =
                    "";

                return;
            }


            selectedFile.textContent =
                "✓ Selected: " +
                file.name;

        }


        // =====================================================
        // DRAG AND DROP
        // =====================================================

        uploadBox.addEventListener(
            "dragover",
            function (event) {

                event.preventDefault();

                uploadBox.classList.add(
                    "dragover"
                );

            }
        );


        uploadBox.addEventListener(
            "dragleave",
            function () {

                uploadBox.classList.remove(
                    "dragover"
                );

            }
        );


        uploadBox.addEventListener(
            "drop",
            function (event) {

                event.preventDefault();

                uploadBox.classList.remove(
                    "dragover"
                );


                const files =
                    event.dataTransfer.files;


                if (
                    files.length > 0
                ) {

                    fileInput.files =
                        files;

                    showSelectedFile();

                }

            }
        );


        // =====================================================
        // FORM SUBMISSION
        // =====================================================

        form.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                errorBox.classList.add(
                    "hidden"
                );

                results.classList.add(
                    "hidden"
                );


                const resumeText =
                    document.getElementById(
                        "resume_text"
                    ).value.trim();


                const hasFile =
                    fileInput.files &&
                    fileInput.files.length > 0;


                if (
                    !hasFile &&
                    !resumeText
                ) {

                    showError(
                        "Please upload a resume or paste your resume text."
                    );

                    return;
                }


                // -------------------------------------------------
                // LOADING
                // -------------------------------------------------

                analyzeButton.disabled =
                    true;

                buttonText.textContent =
                    "Analyzing Resume...";

                loader.classList.remove(
                    "hidden"
                );


                try {

                    const formData =
                        new FormData(
                            form
                        );


                    const response =
                        await fetch(
                            "/analyze",
                            {
                                method: "POST",
                                body: formData
                            }
                        );


                    const data =
                        await response.json();


                    if (
                        !response.ok ||
                        !data.success
                    ) {

                        throw new Error(
                            data.error ||
                            "Unable to analyze resume."
                        );

                    }


                    displayResults(
                        data
                    );


                }
                catch (error) {

                    console.error(
                        error
                    );

                    showError(
                        error.message
                    );

                }
                finally {

                    analyzeButton.disabled =
                        false;

                    buttonText.textContent =
                        "Analyze My Career";

                    loader.classList.add(
                        "hidden"
                    );

                }

            }
        );


        // =====================================================
        // DISPLAY RESULTS
        // =====================================================

        function displayResults(
            data
        ) {

            results.classList.remove(
                "hidden"
            );


            // -------------------------------------------------
            // TOP CAREER
            // -------------------------------------------------

            document.getElementById(
                "topCareer"
            ).textContent =
                data.top_career;


            document.getElementById(
                "topConfidence"
            ).textContent =
                data.top_confidence +
                "%";


            // -------------------------------------------------
            // TOP 5
            // -------------------------------------------------

            const careerList =
                document.getElementById(
                    "careerList"
                );


            careerList.innerHTML =
                "";


            data.predictions.forEach(
                function (
                    prediction,
                    index
                ) {


                    const item =
                        document.createElement(
                            "div"
                        );


                    item.className =
                        "career-item";


                    const hybridScore =
                        Number(
                            prediction.hybrid_score ||
                            prediction.confidence ||
                            0
                        );


                    const rfScore =
                        Number(
                            prediction.random_forest_confidence ||
                            0
                        );


                    const xgbScore =
                        Number(
                            prediction.xgboost_confidence ||
                            0
                        );


                    const alignment =
                        Number(
                            prediction.skill_alignment ||
                            0
                        );


                    item.innerHTML = `

                        <div class="career-header">

                            <span class="career-name">

                                ${index + 1}.
                                ${escapeHtml(
                                    prediction.career
                                )}

                            </span>


                            <span class="career-score">

                                ${hybridScore}%

                            </span>

                        </div>


                        <div class="career-progress">

                            <div
                                class="career-progress-bar"
                                style="width:${Math.min(
                                    hybridScore,
                                    100
                                )}%"
                            ></div>

                        </div>


                        <div class="career-details">

                            <span>
                                Hybrid: ${hybridScore}%
                            </span>

                            <span>
                                Random Forest: ${rfScore}%
                            </span>

                            <span>
                                XGBoost: ${xgbScore}%
                            </span>

                            <span>
                                Skill Alignment: ${alignment}%
                            </span>

                        </div>

                    `;


                    careerList.appendChild(
                        item
                    );

                }
            );


            // -------------------------------------------------
            // IDENTIFIED SKILLS
            // -------------------------------------------------

            renderSkills(
                "identifiedSkills",
                data.identified_skills,
                "skill"
            );


            // -------------------------------------------------
            // MATCHED SKILLS
            // -------------------------------------------------

            renderSkills(
                "matchedSkills",
                data.matched_skills,
                "skill matched"
            );


            // -------------------------------------------------
            // MISSING SKILLS
            // -------------------------------------------------

            renderSkills(
                "missingSkills",
                data.missing_skills,
                "skill missing"
            );


            // -------------------------------------------------
            // SKILL ALIGNMENT
            // -------------------------------------------------

            const alignment =
                Number(
                    data.skill_alignment ||
                    0
                );


            document.getElementById(
                "alignmentValue"
            ).textContent =
                alignment +
                "%";


            document.getElementById(
                "alignmentBar"
            ).style.width =
                Math.min(
                    alignment,
                    100
                ) +
                "%";


            // -------------------------------------------------
            // SCROLL
            // -------------------------------------------------

            results.scrollIntoView({
                behavior:
                    "smooth"
            });

        }


        // =====================================================
        // RENDER SKILLS
        // =====================================================

        function renderSkills(
            elementId,
            skills,
            className
        ) {

            const container =
                document.getElementById(
                    elementId
                );


            container.innerHTML =
                "";


            if (
                !skills ||
                skills.length === 0
            ) {

                container.innerHTML =
                    "<span>No skills identified.</span>";

                return;
            }


            skills.forEach(
                function (skill) {

                    const span =
                        document.createElement(
                            "span"
                        );


                    span.className =
                        className;


                    span.textContent =
                        skill;


                    container.appendChild(
                        span
                    );

                }
            );

        }


        // =====================================================
        // ERROR
        // =====================================================

        function showError(
            message
        ) {

            errorMessage.textContent =
                message;


            errorBox.classList.remove(
                "hidden"
            );


            errorBox.scrollIntoView({
                behavior:
                    "smooth"
            });

        }


        // =====================================================
        // RESET
        // =====================================================

        resetButton.addEventListener(
            "click",
            function () {

                form.reset();

                selectedFile.textContent =
                    "";

                results.classList.add(
                    "hidden"
                );

                errorBox.classList.add(
                    "hidden"
                );

                window.scrollTo({
                    top: 0,
                    behavior:
                        "smooth"
                });

            }
        );


        // =====================================================
        // HTML ESCAPE
        // =====================================================

        function escapeHtml(
            text
        ) {

            const div =
                document.createElement(
                    "div"
                );


            div.textContent =
                text;


            return div.innerHTML;

        }

    }
);