// import image from "../Images/image.png"
import apple from "../Images/a.jpg";
import bee from "../Images/b.jpg";
import cat from "../Images/c.jpg";
import dog from "../Images/d.jpg";
import elephant from "../Images/e.jpg";
import fish from "../Images/f.jpg";
import goat from "../Images/g.jpg";
import hat from "../Images/h.jpg";
import igloo from "../Images/i.jpg";
import jar from "../Images/j.jpg";
import kite from "../Images/k.jpg";
import lion from "../Images/l.jpg";
import mouse from "../Images/m.jpg";
import nest from "../Images/n.jpg";
import octopus from "../Images/o.jpg";
import pig from "../Images/p.jpg";
import quilt from "../Images/q.jpg";
import robot from "../Images/r.jpg";
import snake from "../Images/s.jpg";
import tortoise from "../Images/t.jpg";
import umbrella from "../Images/u.jpg";
import violin from "../Images/v.jpg";
import wagon from "../Images/w.jpg";
import xray from "../Images/x.jpg";
import yarn from "../Images/y.jpg";
import zebra from "../Images/z.jpg";

let _Questions = [
	{
		image: apple,
		solution: "apple",
	},
	{
		image: bee,
		solution: "bee"
	},
	{
		image: cat,
		solution: "cat"
	},
	{
		image: dog,
		solution: "dog"
	},
	{
		image: elephant,
		solution: "elephant",
	},
	{
		image: fish,
		solution: "fish"
	},
	{
		image: goat,
		solution: "goat"
	},
	{
		image: hat,
		solution: "hat"
	},
	{
		image: igloo,
		solution: "igloo",
	},
	{
		image: jar,
		solution: "jar"
	},
	{
		image: kite,
		solution: "kite"
	},
	{
		image: lion,
		solution: "lion"
	},
	{
		image: mouse,
		solution: "mouse",
	},
	{
		image: nest,
		solution: "nest"
	},
	{
		image: octopus,
		solution: "octopus"
	},
	{
		image: pig,
		solution: "pig"
	},
	{
		image: quilt,
		solution: "quilt",
	},
	{
		image: robot,
		solution: "robot"
	},
	{
		image: snake,
		solution: "snake"
	},
	{
		image: tortoise,
		solution: "tortoise"
	},
	{
		image: umbrella,
		solution: "umbrella",
	},
	{
		image: violin,
		solution: "violin"
	},
	{
		image: wagon,
		solution: "wagon"
	},
	{
		image: xray,
		solution: "xray"
	},
	{
		image: yarn,
		solution: "yarn"
	},
	{
		image: zebra,
		solution: "zebra"
	}
];


export const Questions = _Questions.sort((a, b) => (Math.random() - 0.5)).slice(0, 10)
