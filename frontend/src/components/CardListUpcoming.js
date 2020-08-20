import React,{Component} from "react";
import Card from "./Card.js"
import "./CardListUpcoming.css"
import {Link} from "react-router-dom"

var hostUrl="http://localhost:9004/data/"

export default class CardList extends Component{
	constructor(props)
	{
		super(props)
		this.state.category=props.location.state.category
		this.state.group=props.location.state.group
	}
	state={
		productType : "Upcoming",
		category : "",
		group:"",
		cards: []
	}
	// Fetch list of products from the file server and update the state in cards to display all the cards
	componentDidMount() {
        fetch(hostUrl+this.state.productType+"/"+this.state.group+"/"+this.state.category+".json")
        .then((response) => response.json())
        .then(cardsList => {
            this.setState({ cards: cardsList })
        });
    }
	render(){
		// Map the list of JSON products to react components and display them in a grid
		console.log("Render")
		var list=this.state.cards
		console.log(list)
		var processedList=list.map(card=>(<Card name={card.name} keyLabel={card.key} imageSource={card.imageLink} productLink={"http://"+card.productLink}/>))
		return (
			<div>
				<div className="header">
					<Link className="type-header-upcoming1" to={{
			            pathname:"/category/Trending",
			            state:{ 
			            		"group":this.state.group,
			            		"category":this.state.category}
			          }}>
			        	<h2>Trending</h2>
			        </Link>
			        <Link className="type-header-upcoming2" to={{
			            pathname:"/category/Upcoming",
			            state:{ 
			            		"group":this.state.group,
			            		"category":this.state.category}
			          }}>
			        	<h2>Upcoming</h2>
			        </Link>
	      		</div>
				<div className="wrapper">
					{console.log("Updated")}
					{processedList}
				</div>
			</div>
		)
	}	
}