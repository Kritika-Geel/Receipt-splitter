import streamlit as st
from PIL import Image
from schemas import BillData, LineItem
from extractor import parse_receipt
from splitter import calculate_split

st.set_page_config(page_title="Proportional Bill Splitter", layout="wide")
st.title("🧾 Proportional Receipt Splitter")
st.caption("Multimodal bill extraction, human-in-the-loop review, and proportional tax/tip distribution.")

uploaded_file = st.file_uploader("Upload Receipt Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col_img, col_data = st.columns([1, 2])
    image = Image.open(uploaded_file)
    with col_img:
        st.image(image, caption="Uploaded Bill", use_container_width=True)

    # Cache parsing in session state so re-renders don't re-call API
    if "bill_data" not in st.session_state:
        with st.spinner("Extracting line items and charges..."):
            try:
                st.session_state.bill_data = parse_receipt(image)
            except Exception as e:
                st.error(f"Failed to extract bill data: {e}")
                st.stop()

    bill: BillData = st.session_state.bill_data

    with col_data:
        st.subheader("👥 Add Diners")
        raw_friends = st.text_input("Enter names separated by commas:", "Alice, Bob, Charlie")
        friends = [f.strip() for f in raw_friends.split(",") if f.strip()]

        st.subheader("🔍 Review & Correct Items")
        st.info("Edit items or prices if the model made an error. Confidence scores shown per line.")

        assignments = {}
        updated_items = []

        for idx, item in enumerate(bill.items):
            c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 4])
            name = c1.text_input("Item", item.name, key=f"name_{idx}")
            price = c2.number_input("Price", value=float(item.price), step=1.0, key=f"price_{idx}")
            c3.markdown(f"**Conf:** `{item.confidence:.2f}`")
            assigned = c4.multiselect("Diners", options=friends, default=friends, key=f"assigned_{idx}")
            
            assignments[idx] = assigned
            updated_items.append(LineItem(name=name, price=price, quantity=item.quantity, confidence=item.confidence))

        bill.items = updated_items

        st.markdown("---")
        st.subheader("Taxes & Adjustments")
        t1, t2, t3, t4 = st.columns(4)
        bill.subtotal = t1.number_input("Subtotal", value=float(bill.subtotal), step=1.0)
        bill.gst_tax = t2.number_input("GST / Tax", value=float(bill.gst_tax), step=1.0)
        bill.service_charge = t3.number_input("Service Charge", value=float(bill.service_charge), step=1.0)
        bill.discount = t4.number_input("Discount", value=float(bill.discount), step=1.0)

        # Flag printed total discrepancy
        calc_total = bill.subtotal + bill.gst_tax + bill.service_charge - bill.discount
        if abs(calc_total - bill.total_printed) > 0.05:
            st.warning(f"⚠️ Discrepancy detected! Printed Total: ₹{bill.total_printed}, Calculated: ₹{calc_total:.2f}")

        if st.button("Calculate Final Split", type="primary"):
            breakdown = calculate_split(bill, assignments, friends)
            st.subheader("📊 Final Breakdown")
            
            for friend, data in breakdown.items():
                st.success(
                    f"**{friend}**: Food Subtotal = ₹{data['subtotal']:.2f} | "
                    f"Proportional Extra (Taxes & Fees) = ₹{data['proportional_fees']:.2f} | "
                    f"**Total to Pay = ₹{data['total']:.2f}**"
                )