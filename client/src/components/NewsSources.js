import React, { Component } from 'react';
import axios from 'axios'
import { Button, Card, Loader, Segment, Dimmer } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

class NewsSources extends Component {

    constructor() {
        super()
        this.state = {
            news_feeds:{},
            loading: true
        }
    }

    async componentDidMount() {
        const response = await axios.get('/api/user/scrape')
        const feeds = response.data
        this.setState({news_feeds: feeds, loading: false}) 
        console.log(this.state.news_feeds)
       }

    render() {
        const posts = Object.entries(this.state.news_feeds)
        const listURLs = posts.map(([title, url]) =>
        <Card>
            <Card.Content>
                <Card.Header>{title}</Card.Header>
            </Card.Content>
            <Card.Content extra>
            <Link to="route" target="_blank" onClick={(event) => {event.preventDefault(); window.open(url);}}>
                        <Button basic color='green'>
                            Go to Page
                        </Button>
            </Link>
                    
      </Card.Content>
    </Card>
        );

        if (this.state.loading) {
            return (
                <div className="container">
                <div className="jumbotron mt-5">
                        <div class="ui active inverted dimmer">
                            <div class="ui large text loader">Loading</div>
                        </div>
                </div>
                </div>
            )
        }

        return (
            <div className="container">
                <div className="jumbotron mt-5">
                        <h1 className="text-center">Your News For Today: </h1>
                        <Card.Group>
                            {listURLs}
                        </Card.Group>
                </div>
            </div>
        )
    }
}

export default NewsSources;