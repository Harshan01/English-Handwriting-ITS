import React from "react";
import "../../App.css";
import CorrectAnswerPage from "./CorrectAnswerPage";
import IncorrectAnswerPage from "./IncorrectAnswerPage";
import { useState, useEffect } from "react";

function AnswerScreen(props) {
	const {
		solution,
		currentQuestion,
		questionLength,
		finishQuiz,
		nextQuestion,
		answerFile,
		updateScore,
	} = props;
	const [returnedAnswer, setReturnedAnswer] = useState("");
	const [isCorrectAnswer, setIsCorrectAnswer] = useState(false);

	useEffect(() => {
		// make API Request and set answerState and isCorrectAnswer
		// localhost:5000/recognize
		// {"image": "<IMAGE>"}

		if (!answerFile)
			return;

		fetch("http://localhost:5000/recognize", {
			method: "POST",
			headers: {
				Accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				image: answerFile,
			}),
		})
		.then(response => response.json())
		.then(json => {
			setReturnedAnswer(json.submitted_answer);
			let _isCorrect = json.submitted_answer.trim() === solution.trim();
			setIsCorrectAnswer(_isCorrect);
			updateScore(_isCorrect);
		})
		.catch(error => {
			console.error(error);
		});
	}, [answerFile]);

	return (
		<div>
			{returnedAnswer === "" ? (
				<div className="Loading">Loading...</div>
			) : (
				<div>
					<div>
						{isCorrectAnswer ? (
							<CorrectAnswerPage solution={solution}></CorrectAnswerPage>
						) : (
							<IncorrectAnswerPage
								solution={solution}
								returnedAnswer={returnedAnswer}
							></IncorrectAnswerPage>
						)}
					</div>
					<div>
						{currentQuestion === questionLength ? (
							<button onClick={finishQuiz} id="nextQuestion">
								Finish Quiz
							</button>
						) : (
							<button onClick={nextQuestion} id="nextQuestion">
								Next Question
							</button>
						)}
					</div>
				</div>
			)}
		</div>
	);
}

export default AnswerScreen;
