import React from "react";
import "../../App.css";

function QuestionScreen(props) {
	const { question, fileUploader, answerFile, quizStateHandler } = props;

	const fieldSelectedHandler = e => {
		fileUploader(e.target.files[0]);
	};

	const fileUploadHandler = () => {
		if (!answerFile) {
			alert("Please upload a valid file");
		} else {
			quizStateHandler("answer");
		}
	};

	return (
		<div className="question-container">
			<div className="question-image">
				<img src={question} alt="Question" width="400px" />
			</div>
			<br/><br/>
			<div className="image-upload">
				<div>
					<input type="file" onChange={e => fieldSelectedHandler(e)}></input>
				</div>
				<div>
					<button onClick={fileUploadHandler} id="nextQuestion">
						Upload
					</button>
				</div>
			</div>
		</div>
	);
}

export default QuestionScreen;
