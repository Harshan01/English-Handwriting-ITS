import React from "react";
import "../../App.css";

function IncorrectAnswerPage({ returnedAnswer, solution }) {
	return (
		<div>
			<h2>Incorrect Answer!</h2>
			<p>Your Answer = {returnedAnswer}</p>
			<p>Correct Answer = {solution}</p>
		</div>
	);
}

export default IncorrectAnswerPage;
