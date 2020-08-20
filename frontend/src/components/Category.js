import React,{Component} from "react"
import './Category.css'
import {Link} from "react-router-dom"

export default class Category extends Component{
	constructor(props){
		super(props)
		this.group=props.group
		this.category=props.category
	}
	render(){
		var imageLink="http://localhost:9004/categoryImages/"+this.group+"/"+this.category+".jpg"
		// Address of cateogry image on file server

		// Add link of category page (with group and category as state) to the image
		return (
			<div key={this.group+this.category} className="card-container">
				<Link className="textDecorator" to={{
		            pathname:"/category/Trending",
		            state:{ 
		            		"group":this.group,
		            		"category":this.category}
		          }}
		        >
		        	<img src={imageLink} alt={this.category} className="card-image"/>
		        </Link>
		        <h2>{this.category}</h2>
			</div>
		)
	}
}