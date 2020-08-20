import React,{Component} from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import "./CategoryGrid.css"
import CategoryCard from "./Category"

const categories={"Men":["Shirts","Tshirts"],
				  "Women":["Western Dress","Tops and Tshirts","Jumpsuits","Ethnic Dress"]
				}

export default class CategoryGrid extends Component{
	constructor(props)
	{
		super(props)
		this.group=props.group
	}
	render(){
		var processedList=categories[this.group].map(category=>(<CategoryCard group={this.group} category={category}/>));
		// Create react components for all categories of the procided group

		// Display group Title along with the grid of categories
		return (
			<div className="container">
				<h1>{this.group}</h1>
				<div className="wrapper">
					{processedList}
				</div>
			</div>
		)
	}	
}
