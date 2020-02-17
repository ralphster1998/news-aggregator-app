import React, { Component } from 'react';

const data = [{
        name: 'www.yahoo.com',
        value: 'www.yahoo.com'
    },
    {
        name: 'www.medicalnewstoday.com',
        value: 'www.medicalnewstoday.com'
    },
    {
        name: 'https://www.buzzfeednews.com/section/books',
        value: 'https://www.buzzfeednews.com/section/books'
    }];

class NewsSources extends Component {
    result(params) {
        console.log(params);
    }

    render () {
        return (
            <div className="container">
                <div className="jumbotron mt-5">
                    <div className="col-sm-8 mx-auto">
                        <h1 className="text-center">Your News Will Show Up Here</h1>
                    </div>
                </div>
            </div>
        )
    }
}

export default NewsSources;