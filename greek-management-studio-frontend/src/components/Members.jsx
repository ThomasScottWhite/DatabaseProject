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
      const response = await user.get_with_headers(
        "/api/chapter/" + user.user.chapter_id + "/members"
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);
      setMembers(data);
      setEditableMembers(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const EditUser = async (updatedMember) => {
    try {
      const updatedMemberCopy = { ...updatedMember };
      delete updatedMemberCopy.chapter_id;
      delete updatedMemberCopy.email;

      const response = await user.patch_with_headers(
        `/api/member/${updatedMember.email}`,
        updatedMemberCopy
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await Refresh();
    } catch (error) {
      console.error("Error updating member:", error);
    }
  };

  const handleInputChange = (member_id, field, value) => {
    setEditableMembers((prev) =>
      prev.map((member) =>
        member.member_id === member_id ? { ...member, [field]: value } : member
      )
    );
  };

  const handleSubmit = (member_id) => {
    const updatedMember = editableMembers.find(
      (member) => member.member_id === member_id
    );
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
          <Col xs={12} md={6} lg={4} key={member.member_id} className="mb-4">
            <Card>
              <Card.Body>
                {editMode ? (
                  <>
                    <Form.Group className="mb-2">
                      <Form.Label>First Name</Form.Label>
                      <Form.Control
                        type="text"
                        value={member.fname}
                        onChange={(e) =>
                          handleInputChange(
                            member.member_id,
                            "fname",
                            e.target.value
                          )
                        }
                      />
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Last Name</Form.Label>
                      <Form.Control
                        type="text"
                        value={member.lname}
                        onChange={(e) =>
                          handleInputChange(
                            member.member_id,
                            "lname",
                            e.target.value
                          )
                        }
                      />
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Member Status</Form.Label>
                      <Form.Control
                        type="text"
                        value={member.member_status}
                        onChange={(e) =>
                          handleInputChange(
                            member.member_id,
                            "member_status",
                            e.target.value
                          )
                        }
                      />
                    </Form.Group>
                    <Form.Group className="mb-2">
                      <Form.Label>Phone Number</Form.Label>
                      <Form.Control
                        type="text"
                        value={member.phone_num}
                        onChange={(e) =>
                          handleInputChange(
                            member.member_id,
                            "phone_num",
                            e.target.value
                          )
                        }
                      />
                    </Form.Group>
                    {user.user.is_admin && (
                      <Form.Group className="mb-2">
                        <Form.Check
                          type="checkbox"
                          label="Is Chapter Admin"
                          checked={member.is_chapter_admin}
                          onChange={(e) =>
                            handleInputChange(
                              member.member_id,
                              "is_chapter_admin",
                              e.target.checked
                            )
                          }
                        />
                      </Form.Group>
                    )}
                    <Button
                      variant="success"
                      onClick={() => handleSubmit(member.member_id)}
                    >
                      Submit
                    </Button>
                  </>
                ) : (
                  <>
                    <Card.Title>{member.fname + " " + member.lname}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">
                      {member.member_status}
                    </Card.Subtitle>
                    <Card.Text>Email: {member.email}</Card.Text>
                    <Card.Text>Phone Number: {member.phone_num}</Card.Text>
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
