import React, { useState, useEffect } from "react";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { useUser } from "../context/user_context";

const MakeBills = () => {
  const [dueDate, setDueDate] = useState(
    new Date().toISOString().split("T")[0]
  );
  const [desc, setDesc] = useState(""); // Description (Bill Name)
  const [amount, setAmount] = useState("");
  const [memberEmail, setMemberEmail] = useState("");
  const [invoiceOptions, setInvoiceOptions] = useState([]); // For dropdown options
  const user = useUser();

  // Fetch the list of members
  useEffect(() => {
    const fetchMembers = async () => {
      try {
        const response = await user.get_with_headers(
          `/api/chapter/${user.user.chapter_id}/members`
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        const formattedOptions = data.map((member) => ({
          value: member.email, // Use email as the value
          label: `${member.fname} ${member.lname} (${member.email})`,
        }));
        setInvoiceOptions(formattedOptions);
      } catch (error) {
        console.error("Error fetching members:", error);
        alert("An error occurred while fetching member options.");
      }
    };

    fetchMembers();
  }, [user]);

  const makeBillRequest = async (e) => {
    e.preventDefault();

    if (!memberEmail) {
      alert("Please select a member.");
      return;
    }

    const payload = {
      chapter_id: user.user.chapter_id,
      amount: parseFloat(amount), // Ensure amount is a number
      desc, // Use the description field
      due_date: dueDate,
      member_email: memberEmail, // Selected member's email
    };

    try {
      const response = await user.post_with_headers(
        "/api/bill/internal",
        payload
      );
      if (response.ok) {
        alert("Bill Created Successfully");
      } else {
        const errorData = await response.json();
        console.error("Error:", errorData);
        alert("Failed to create bill.");
      }
    } catch (error) {
      console.error("Error creating bill:", error);
      alert("An error occurred while creating the bill.");
    }
  };

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col xs={12} md={6}>
          <h2 className="text-center">Create a Bill</h2>
          <Form onSubmit={makeBillRequest}>
            <Form.Group controlId="formDesc" className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter bill description"
                value={desc}
                onChange={(e) => setDesc(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="formMemberEmail" className="mb-3">
              <Form.Label>Member</Form.Label>
              <Form.Control
                as="select"
                value={memberEmail}
                onChange={(e) => setMemberEmail(e.target.value)}
                required
              >
                <option value="" disabled>
                  Select Member
                </option>
                {invoiceOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="formDueDate" className="mb-3">
              <Form.Label>Due Date</Form.Label>
              <Form.Control
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="formAmount" className="mb-3">
              <Form.Label>Amount</Form.Label>
              <Form.Control
                type="number"
                placeholder="Enter amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100">
              Submit
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default MakeBills;
