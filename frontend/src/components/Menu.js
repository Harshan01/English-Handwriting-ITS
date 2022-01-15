import React from "react";
import "../App.css";
import { useContext } from "react";
import { GameStateContext } from "../helpers/Contexts";

function Menu() {
	const { setGameState, setUserName } = useContext(GameStateContext);
	return (
		<div className="Menu">
			<label>Enter Your Name:</label>
			<input
				type="text"
				placeholder="Name"
				onChange={event => {
					setUserName(event.target.value);
				}}
			/>
			<button
				onClick={() => {
					setGameState("playing");
				}}
			>
				Start Quiz
			</button>
		</div>
	);
}

export default Menu;
