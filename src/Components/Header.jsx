import React, { Component } from 'react';
import {Navbar , Nav ,Form, FormControl , Button} from 'react-bootstrap';

const Header =  ()  => {
    return (
      <Navbar
        bg ="dark"
        variant="dark"
        sticky="top"
        style={{
          // border: "3px solid white",
          padding: "0px",
          margin: "0px",
          borderRadius: "0px",
          backgroundColor: "#ebebf5",
          padding: "0.5em",
          height:"5em",
          boxShadow: "0px 2px 8px #9f9fa6"
        }}
      >
        <Navbar.Brand href="#home" style={{ padding: "2px", display:"flex" }}>
          {/* <img src={process.env.PUBLIC_URL + "/code.jpg"} width="30px" heigth="30px" /> */}
          <div style={{}}>
          CMJudge
          </div>
        </Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="#home">Home</Nav.Link>
          <Nav.Link href="#features">Assignments</Nav.Link>
          <Nav.Link href="#pricing">Profile</Nav.Link>
        </Nav>

        <Form inline>
          {/* <FormControl type="text" placeholder="Search" className="mr-sm-2" /> */}
          <Button variant="outline-info">Sign Out</Button>
        </Form>
      </Navbar>
    );  
};

export default Header;