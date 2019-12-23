import React, { PureComponent } from "react";
import {
  Container,
  Navbar,
  Nav,
  Form,
  FormControl,
  Button
} from "react-bootstrap";

const content = `Input Sample <br> yahh <br> is not aligned i guess`;
const Output = e => {
  return (
    <div
      style={{
        paddingTop: "0.2em",
        marginLeft: "1.2em"
      }}
    >
      <Container
        style={{
          height: "auto",
          boxShadow: "-1px 0px 2px #d4d2d2",
          boxShadow: "1px 0px 2px #d4d2d2",
          borderRadius: "10px",
          borderLeft: "1px solid #d4d2d2",
          paddingLeft: "0px",
          margin: "1em",
          padding: "0px",
          backgroundColor: "#ffffff",
          width: "60%",
          borderBottom: "1px solid #d4d2d2",

          fontSize: "1.2vw",

          paddingTop: "0px"
        }}
      >
        <div
          style={{
            padding: "0px",
            margin: "0px",
            height: "auto"
          }}
        >
          <Navbar
            sticky="True"
            style={{
              borderTopLeftRadius: "10px",
              borderTopRightRadius: "10px",
              backgroundColor: "#115"
            }}
          >
            <Nav className="mr-auto">
              <h6
                style={{
                  paddingLeft: "1.2em",
                  paddingTop: "0.5em",
                  color: "white",
                  borderRadius: "10px"
                }}
              >
                Output Sample
              </h6>
            </Nav>
          </Navbar>
          <p
            style={{
              padding: "3em",
              textAlign: "justify",
              fontSize: "1.45em",
              paddingLeft: "1em",
              paddingTop: "1.5em"
            }}
          >
            {content}
          </p>
        </div>
      </Container>
    </div>
  );
};

export default Output;
