import React, { Component } from 'react';
import axios from 'axios'
import { Button, Card, Loader, Segment, Dimmer } from 'semantic-ui-react'

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
                <Card.Description>
                {url}
                </Card.Description>
            </Card.Content>
            <Card.Content extra>
                <div className='ui two buttons'>
                    <Button basic color='green'>
                        Go to Page
                    </Button>
                </div>
      </Card.Content>
    </Card>
        );

        if (this.state.loading) {
            return (
                <Segment>

                    <Dimmer active>
                    <Loader />
                    </Dimmer>
                    
                </Segment>
            )
        }

        return (
            <div className="container">
                <div className="jumbotron mt-5">
                    <div className="col-sm-8 mx-auto">
                        <h1 className="text-center">Your News For Today: </h1>
                        <Card.Group>
                            {listURLs}
                        </Card.Group>
                    </div>
                </div>
            </div>
        )
    }
}

export default NewsSources;