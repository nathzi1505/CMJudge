import React, { PureComponent } from 'react';
import {Container, Navbar, Nav, Form, FormControl, Button } from "react-bootstrap";


const content = `
    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" The Extremes of Good and Evil by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.

The standardrem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don\'t look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn\'t anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.
`

const sm_content = `
      Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

`;

const Question = e => {
  
  return (
    <div
      style={{
        paddingTop: "1.5em",
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
          borderBottom:"1px solid #d4d2d2",
          paddingLeft: "0px",
          margin: "1em",
          padding: "0px",
          backgroundColor: "#ffffff",
          width: "60%",

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
          <Navbar sticky="True" style={{
            borderTopLeftRadius:"10px",
            borderTopRightRadius:"10px",
            backgroundColor:"#115",
            }}>
            <Nav className="mr-auto">
              <h2
                style={{
                  paddingLeft: "1.2em",
                  paddingTop: "0.5em",
                  color:"white",
                  borderRadius:"10px"
                }}
              >
                Placeholder title
              </h2>
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
            {sm_content}
          </p>
        </div>
      </Container>
    </div>
  );
};

export default Question;