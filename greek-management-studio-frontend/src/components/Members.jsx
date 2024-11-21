import React, { useState, useEffect } from "react";
import { Card, Container, Row, Col, Button } from "react-bootstrap";
import { useUser } from "../context/user_context";

const Members = () => {
  const user = useUser();
  const [members, setMembers] = useState(null);

  const payload = { someKey: "someValue" };

  const Refresh = async () => {
    try {
      const response = await user.get_with_headers("/api/homepage");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setMembers(data.members);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    Refresh();
  }, []);

  if (members === null) {
    return <h2>Loading...</h2>;
  }
  return (
    <Container className="mt-5">
      <h2 className="text-center mb-4">Organization Members</h2>
      <Row>
        {members.map((member) => (
          <Col xs={12} md={6} lg={4} key={member.id} className="mb-4">
            <Card>
              <Card.Body>
                <Card.Title>{member.name}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">
                  {member.role}
                </Card.Subtitle>
                <Card.Text>Email: {member.email}</Card.Text>
                <Button variant="primary">View Profile</Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default Members;
