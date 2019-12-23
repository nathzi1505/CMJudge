import React, { Component } from 'react';

import Header from "../Components/Header";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";

// import logo from "../public/code.jpg";
import Fade from "react-reveal/Fade";
import Assg from "../Components/Assignment";
import Question from "../Components/Question";
import User from "../Components/user";
import Input from "../Components/Input";
import Output from "../Components/Output";
import { Button } from "react-bootstrap";


const Page = e =>{

    return (
      <div
        style={{
          // backgroundColor: "#f0f0f2",
          height: "100%",
          width: "100%"
        }}
      >
        <Header />
        <Fade bottom>
          <Assg />
        </Fade>
        <Question />
        <User />
        <Input />
        <Output />
        <Button
          variant="outline-success"
          size="lg"
          style={{
            margin: "2em",
            marginTop: "1.5em"
          }}
        >
          Submit
        </Button>
      </div>
    );
}

export default Page;