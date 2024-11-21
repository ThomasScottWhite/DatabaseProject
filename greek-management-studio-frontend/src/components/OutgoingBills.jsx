import React, { useState, useEffect } from "react";
import { Table, Container, Button, Form } from "react-bootstrap";
import { useUser } from "../context/user_context";

const ViewBills = () => {
  const [bills, setBills] = useState(null);
  const [editableBills, setEditableBills] = useState([]);
  const [editMode, setEditMode] = useState(false);
  const user = useUser();

  const Refresh = async () => {
    try {
      const response = await user.get_with_headers("/api/outgoing-bills");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setBills(data.bills);
      setEditableBills(data.bills); // Initialize editableBills
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const EditBill = async (updatedBill) => {
    try {
      const response = await user.post_with_headers(
        `/api/update_bill/${updatedBill.invoicee_id}`,
        updatedBill
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await Refresh(); // Refresh data after update
    } catch (error) {
      console.error("Error updating bill:", error);
    }
  };

  const handleInputChange = (id, field, value) => {
    setEditableBills((prev) =>
      prev.map((bill) =>
        bill.invoicee_id === id ? { ...bill, [field]: value } : bill
      )
    );
  };

  const handleSubmit = (id) => {
    const updatedBill = editableBills.find((bill) => bill.invoicee_id === id);
    if (updatedBill) {
      EditBill(updatedBill);
    }
  };

  useEffect(() => {
    Refresh();
  }, []);

  if (bills === null) {
    return <h2>Loading...</h2>;
  }

  return (
    <Container className="mt-5">
      <h2 className="text-center mb-4">Outgoing Bills</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Invoicee</th>
            <th>Bill Name</th>
            <th>Amount ($)</th>
            <th>Due Date</th>
            {editMode && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {editableBills.map((bill) => (
            <tr key={bill.invoicee_id}>
              <td>{bill.invoicee_id}</td>
              <td>
                {editMode ? (
                  <Form.Control
                    type="text"
                    value={bill.invoicee_name}
                    onChange={(e) =>
                      handleInputChange(bill.invoicee_id, "invoicee_name", e.target.value)
                    }
                  />
                ) : (
                  bill.invoicee_name
                )}
              </td>
              <td>
                {editMode ? (
                  <Form.Control
                    type="text"
                    value={bill.bill_name}
                    onChange={(e) =>
                      handleInputChange(bill.invoicee_id, "bill_name", e.target.value)
                    }
                  />
                ) : (
                  bill.bill_name
                )}
              </td>
              <td>
                {editMode ? (
                  <Form.Control
                    type="number"
                    value={bill.amount}
                    onChange={(e) =>
                      handleInputChange(bill.invoicee_id, "amount", e.target.value)
                    }
                  />
                ) : (
                  bill.amount
                )}
              </td>
              <td>
                {editMode ? (
                  <Form.Control
                    type="date"
                    value={bill.date}
                    onChange={(e) =>
                      handleInputChange(bill.invoicee_id, "date", e.target.value)
                    }
                  />
                ) : (
                  bill.date
                )}
              </td>
              {editMode && (
                <td>
                  <Button
                    variant="success"
                    size="sm"
                    onClick={() => handleSubmit(bill.invoicee_id)}
                  >
                    Submit
                  </Button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </Table>
      <div className="text-center mt-4">
        <Button onClick={() => setEditMode(!editMode)}>
          {editMode ? "Cancel Edit" : "Edit Bills"}
        </Button>
      </div>
    </Container>
  );
};

export default ViewBills;
