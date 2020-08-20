import React,{Component} from "react"
import './Card.css'

export default class Card extends Component{
	constructor(props){
		super(props)
		this.title=props.name
		this.key=props.keyLabel
		this.imageSource=props.imageSource
		this.productLink=props.productLink
	}
	render(){
		return (
			<div key={this.key} className="card-container">
				<a href={this.productLink} className="textDecorator">
					<img src={this.imageSource} alt={this.title} className="card-image"/>
				</a>
				<h2 className="textDecorator">{this.title}</h2>
			</div>
		)
	}
}