import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import {Card} from 'react-bootstrap';
import { Button } from 'react-bootstrap';


class User extends React.Component{
    constructor(props){
        super(props);

    }
    render(){
        return (
          <div style ={{
              position:"absolute",
              top:"14.9em",
              left:"65%",
          }}>
            <Card style={{ width: "14rem" , heigth:"14em" }}>
              
              <Card.Body>
                <Card.Title >User Info</Card.Title>
                <Card.Text>
                  User Info blah blah
                  djfhndl
                  dhfjkbd
                  hjdbf
                  hdhfd
                </Card.Text>
                <Button variant="primary">Profile</Button>
              </Card.Body>
            </Card>
          </div>
        );
    }
}

export default User;