import React from "react";
import "../../App.css";

function CorrectAnswerPage({ solution }) {
	return (
		<div>
			<h2>Correct Answer!</h2>
			<p>{solution}</p>
		</div>
	);
}

export default CorrectAnswerPage;
