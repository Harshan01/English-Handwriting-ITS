import React from "react";
import "../App.css";
import { Questions } from "../helpers/Images";
import { useState } from "react";
import { useContext } from "react";
import { GameStateContext } from "../helpers/Contexts";
import QuestionScreen from "./Quiz/QuestionScreen";
import AnswerScreen from "./Quiz/AnswerScreen";

function Quiz() {
	const [quizState, setQuizState] = useState("question");
	const [currentQuestion, setCurrentQuestion] = useState(0);
	const [answerFile, setAnswerFile] = useState(null);
	const { score, setScore, setGameState } = useContext(GameStateContext);

	const fileUploader = file => {
		// Convert image to Base64, remove header and upload
		let reader = new FileReader();
		reader.readAsDataURL(file);
		reader.onload = function () {
			setAnswerFile(reader.result.split(",")[1]);
		};
		reader.onerror = function (error) {
			console.log("Error: ", error);
		};
	};

	const quizStateHandler = str => {
		setQuizState("answer");
	};

	const finishQuiz = () => {
		setAnswerFile(null);
		setQuizState("question");
		setGameState("finished");
	};

	const updateScore = isCorrectAnswer => {
		if (isCorrectAnswer) setScore(score + 1);
	};

	const nextQuestion = () => {
		setCurrentQuestion(currentQuestion + 1);
		setAnswerFile(null);
		setQuizState("question");
	};

	return (
		<div className="Quiz">
			{quizState === "question" && (
				<QuestionScreen
					question={Questions[currentQuestion].image}
					answerFile={answerFile}
					fileUploader={fileUploader}
					quizStateHandler={quizStateHandler}
				></QuestionScreen>
			)}
			{quizState === "answer" && (
				<AnswerScreen
					solution={Questions[currentQuestion].solution}
					currentQuestion={currentQuestion}
					questionLength={Questions.length - 1}
					nextQuestion={nextQuestion}
					finishQuiz={finishQuiz}
					answerFile={answerFile}
					updateScore={updateScore}
				></AnswerScreen>
			)}
		</div>
	);
}

export default Quiz;
