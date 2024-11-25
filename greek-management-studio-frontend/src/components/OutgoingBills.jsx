import React, { useState, useEffect } from "react";
import { Table, Container, Button, Modal, Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/user_context";

const ViewBills = () => {
  const [bills, setBills] = useState(null); // Initialize with null to indicate loading state
  const [selectedBill, setSelectedBill] = useState(null); // Bill to edit
  const [showEditModal, setShowEditModal] = useState(false); // Modal visibility
  const [editData, setEditData] = useState({});
  const user = useUser();
  const navigate = useNavigate();

  const Refresh = async () => {
    try {
      const memberEmail = user.user.email; // Get the member email from user context
      const response = await user.get_with_headers(
        `/api/member/${memberEmail}/bills`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setBills(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    Refresh();
  }, []);

  const handlePay = (bill) => {
    navigate(`/payment/${bill.bill_id}/${bill.amount}/${bill.desc}`);
  };

  const handleEdit = (bill) => {
    setSelectedBill(bill);
    setEditData(bill); // Initialize with current bill data
    setShowEditModal(true); // Show the modal
  };

  const handleSaveEdit = async () => {
    try {
      const response = await user.patch_with_headers(
        `/api/bill/internal/${selectedBill.bill_id}`,
        editData
      );

      if (response.ok) {
        setShowEditModal(false);
        Refresh();
      } else {
        console.error("Failed to save edits:", response.statusText);
      }
    } catch (error) {
      console.error("Error saving edits:", error);
    }
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditData((prevData) => ({ ...prevData, [name]: value }));
  };

  if (bills === null) {
    return (
      <Container className="mt-5">
        <h2 className="text-center mb-4">Loading Bills...</h2>
      </Container>
    );
  }

  return (
    <Container className="mt-5">
      <h2 className="text-center mb-4">View Bills</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Bill Id</th>
            <th>Description</th>
            <th>Amount ($)</th>
            <th>Due Date</th>
            <th>Issue Date</th>
            <th>Source</th>
            <th>Paid</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {bills.map((bill, index) => (
            <tr key={bill.bill_id}>
              <td>{index + 1}</td>
              <td>{bill.bill_id}</td>
              <td>{bill.desc}</td>
              <td>{bill.amount}</td>
              <td>{new Date(bill.due_date).toLocaleDateString()}</td>
              <td>{new Date(bill.issue_date).toLocaleDateString()}</td>
              <td>{bill.is_external ? "External" : "Internal"}</td>
              <td>{bill.amount_paid > 0 ? "Yes" : "No"}</td>
              <td>
                {bill.amount_paid === 0 && (
                  <Button variant="success" onClick={() => handlePay(bill)}>
                    Pay
                  </Button>
                )}
                <Button variant="warning" onClick={() => handleEdit(bill)}>
                  Edit
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Edit Modal */}
      {selectedBill && (
        <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
          <Modal.Header closeButton>
            <Modal.Title>Edit Bill</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group>
                <Form.Label>Description</Form.Label>
                <Form.Control
                  type="text"
                  name="desc"
                  value={editData.desc}
                  onChange={handleEditChange}
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>Amount</Form.Label>
                <Form.Control
                  type="number"
                  name="amount"
                  value={editData.amount}
                  onChange={handleEditChange}
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>Due Date</Form.Label>
                <Form.Control
                  type="date"
                  name="due_date"
                  value={
                    new Date(editData.due_date).toISOString().split("T")[0]
                  }
                  onChange={handleEditChange}
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>Issue Date</Form.Label>
                <Form.Control
                  type="date"
                  name="issue_date"
                  value={
                    new Date(editData.issue_date).toISOString().split("T")[0]
                  }
                  onChange={handleEditChange}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowEditModal(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleSaveEdit}>
              Save Changes
            </Button>
          </Modal.Footer>
        </Modal>
      )}
    </Container>
  );
};

export default ViewBills;
