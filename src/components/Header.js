import { Header, Button } from 'semantic-ui-react'
import { Component } from 'react'

class HeaderContent extends Component {
    
    render() {
        return (
            <div style={{ display: "inline" }}>
                <Header 
                    as='h2'
                    style={{marginTop: "30px", marginBottom: "30px" }}
                >
                    EDA Integration
                </Header>
            </div>
        );
    }
}

export default HeaderContent;