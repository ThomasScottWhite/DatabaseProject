import React, { useState, useEffect } from "react";
import { Card, Container, Row, Col, Button, Form } from "react-bootstrap";
import { useUser } from "../context/user_context";

const Members = () => {
  const user = useUser();
  const [members, setMembers] = useState(null);
  const [editableMembers, setEditableMembers] = useState([]);
  const [editMode, setEditMode] = useState(false);

  const Refresh = async () => {
    try {
      const response = await user.get_with_headers("/api/homepage");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setMembers(data.members);
      setEditableMembers(data.members); // Initialize editableMembers
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const EditUser = async (updatedMember) => {
    try {
      const response = await user.post_with_headers(
        `/api/update_member/${updatedMember.id}`,
        updatedMember
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await Refresh(); // Refresh data after update
    } catch (error) {
      console.error("Error updating member:", error);
    }
  };

  const handleInputChange = (id, field, value) => {
    setEditableMembers((prev) =>
      prev.map((member) =>
        member.id === id ? { ...member, [field]: value } : member
      )
    );
  };

  const handleSubmit = (id) => {
    const updatedMember = editableMembers.find((member) => member.id === id);
    if (updatedMember) {
      EditUser(updatedMember);
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
        {editableMembers.map((member) => (
          <Col xs={12} md={6} lg={4} key={member.id} className="mb-4">
            <Card>
              <Card.Body>
                {editMode ? (
                  <>
                    <Form.Group className="mb-2">
                      <Form.Label>Name</Form.Label>
                      <Form.Control
                        type="text"
                        value={member.name}
                        onChange={(e) =>
                          handleInputChange(member.id, "name", e.target.value)
                        }
                      />
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Role</Form.Label>
                      <Form.Control
                        type="text"
                        value={member.role}
                        onChange={(e) =>
                          handleInputChange(member.id, "role", e.target.value)
                        }
                      />
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Email</Form.Label>
                      <Form.Control
                        type="email"
                        value={member.email}
                        onChange={(e) =>
                          handleInputChange(member.id, "email", e.target.value)
                        }
                      />
                    </Form.Group>
                    <Button
                      variant="success"
                      onClick={() => handleSubmit(member.id)}
                    >
                      Submit
                    </Button>
                  </>
                ) : (
                  <>
                    <Card.Title>{member.name}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">
                      {member.role}
                    </Card.Subtitle>
                    <Card.Text>Email: {member.email}</Card.Text>
                    <Button variant="primary">View Profile</Button>
                  </>
                )}
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
      <div className="text-center mt-4">
        <Button onClick={() => setEditMode(!editMode)}>
          {editMode ? "Cancel Edit" : "Edit Members"}
        </Button>
      </div>
    </Container>
  );
};

export default Members;
