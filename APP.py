import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

st.set_page_config(
    page_title="CampusLoop",
    page_icon="♻️",
    layout="wide",
)

st.title("♻️ CampusLoop")
st.subheader("Your campus. Your community. Reuse more.")
st.write("Buy, exchange, or give away pre-owned college items.")
st.caption("A student-powered marketplace for a more sustainable campus.")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase credentials missing. Check your .env file.")
    st.stop()

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.table("listings").select("id").limit(1).execute()
except Exception as e:
    st.error(f"Could not connect to Supabase: {e}")
    st.stop()


def get_listings():
    response = (
        supabase.table("listings")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


browse_tab, create_tab, requests_tab = st.tabs(
    ["🔎 Browse Marketplace", "➕ Create Listing", "💬 Exchange Requests"]
)

with browse_tab:
    st.header("Discover campus finds")

    try:
        listings = get_listings()
    except Exception as e:
        st.error(f"Could not load listings: {e}")
        listings = []

    search = st.text_input(
     "Search items",
     placeholder="Try books, calculator, backpack...",
)

    categories = ["All"] + sorted(
      {item["category"] for item in listings if item.get("category")}
)

    selected_category = st.selectbox("Category", categories)

    sort_by = st.selectbox(
      "Sort listings",
      ["Newest first", "Price: low to high", "Price: high to low"],
)

    filtered = [
      item for item in listings
      if (
        not search
        or search.lower() in item.get("title", "").lower()
        or search.lower() in item.get("description", "").lower()
    )
      and (
        selected_category == "All"
        or item.get("category") == selected_category
    )
]
    

    if sort_by == "Price: low to high":
        filtered.sort(key=lambda x: float(x.get("price") or 0))
    elif sort_by == "Price: high to low":
        filtered.sort(
            key=lambda x: float(x.get("price") or 0), reverse=True
        )

    st.write(f"**{len(filtered)} available item(s)**")

    if not filtered:
        st.info("No matching items yet. Create the first listing!")
    else:
        columns = st.columns(3)

        for index, item in enumerate(filtered):
            with columns[index % 3]:
                with st.container(border=True):
                    image_url = item.get("image_url")
                    if image_url:
                        st.image(image_url, use_container_width=True)

                    st.subheader(item["title"])
                    st.caption(
                        f'{item["category"]} · {item["condition"]}'
                    )
                    price = float(item.get("price") or 0)
                    st.markdown(
                        "**FREE**" if price == 0 else f"**₹{price:,.2f}**"
                    )
                    st.write(item["description"])
                    st.caption(f'Listed by {item["owner_name"]}')

                    with st.expander("Request this item"):
                        with st.form(f'request_{item["id"]}'):
                            requester = st.text_input("Your name")
                            message = st.text_area(
                                "Message to the owner",
                                placeholder="Hi! Is this item still available?",
                            )
                            sent = st.form_submit_button("Send request")

                            if sent:
                                if not requester.strip() or not message.strip():
                                    st.warning("Enter your name and message.")
                                else:
                                    try:
                                        supabase.table(
                                                "exchange_requests"
                                                         ).insert({
                                                      "listing_id": item["id"],
                                                       "requester_name": requester.strip(),
                                                       "message": message.strip(),
                                             }, returning="minimal").execute()
                                        st.success("Request sent!")
                                    except Exception as e:
                                        st.error(f"Request failed: {e}")

                    with st.expander("Update item status"):
                        new_status = st.selectbox(
                            "Status",
                            ["Available", "Reserved", "Completed"],
                            key=f'status_{item["id"]}',
                        )
                        if st.button(
                            "Save status",
                            key=f'save_{item["id"]}',
                        ):
                            try:
                                supabase.table("listings").update(
                                    {"status": new_status}
                                ).eq("id", item["id"]).execute()
                                st.success("Status updated. Refresh the page.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Update failed: {e}")
                    st.subheader("Exchange Requests")
######################
                    try:
                     response = (
                        supabase.table("exchange_requests")
                        .select("*")
                        .order("created_at", desc=True)
                        .execute()
                                )

                     if response.data:
                         st.dataframe(
                           response.data,
                             use_container_width=True
                                )
                     else:
                       st.info("No exchange requests yet.")

                    except Exception as e:
                      st.error(f"Could not load requests: {e}")

with create_tab:
    st.header("Give your items a second life")
    st.write("Add an item for other students to discover.")

    with st.form("create_listing", clear_on_submit=True):
        title = st.text_input("Item name *")
        description = st.text_area("Description *")
        category = st.selectbox(
            "Category",
            [
                "Books & Notes",
                "Electronics",
                "Stationery",
                "Hostel Essentials",
                "Clothing",
                "Other",
            ],
        )
        condition = st.selectbox(
            "Condition",
            ["New", "Like New", "Good", "Fair"],
        )
        price = st.number_input(
            "Price in ₹ (enter 0 for free)",
            min_value=0.0,
            value=0.0,
            step=10.0,
        )
        owner_name = st.text_input("Display name *")
        image_url = st.text_input(
            "Image URL (optional)",
            placeholder="https://example.com/item.jpg",
        )
        submitted = st.form_submit_button("Publish Listing")

        if submitted:
            if not title.strip() or not description.strip() or not owner_name.strip():
                st.warning("Please fill in all required fields.")
            else:
                try:
                    supabase.table("listings").insert({
                        "title": title.strip(),
                        "description": description.strip(),
                        "category": category,
                        "condition": condition,
                        "price": price,
                        "owner_name": owner_name.strip(),
                        "image_url": image_url.strip() or None,
                        "status": "Available",
                    }).execute()
                    st.success("Your listing has been published!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not publish listing: {e}")

with requests_tab:
    st.header("Exchange Requests")
    st.write(
        "Requests are saved in the database. "
        "This prototype does not yet include owner-only request inboxes."
    )

    try:
        request_listings = get_listings()
        request_listing_map = {
            item["id"]: item["title"] for item in request_listings
        }

        if request_listing_map:
            selected_id = st.selectbox(
                "Choose an item to view its requests",
                list(request_listing_map.keys()),
                format_func=lambda item_id: request_listing_map[item_id],
            )

            response = (
                supabase.table("exchange_requests")
                .select("*")
                .eq("listing_id", selected_id)
                .order("created_at", desc=True)
                .execute()
            )

            if response.data:
                for request in response.data:
                    with st.container(border=True):
                        st.write(f'**From:** {request["requester_name"]}')
                        st.write(request["message"])
                        st.caption(f'Status: {request["status"]}')
            else:
                st.info("No requests for this item yet.")
        else:
            st.info("Create a listing first to start receiving requests.")

    except Exception as e:
        st.error(
            "Could not load requests. Check your exchange_requests "
            f"table permissions. Details: {e}"
        )

st.divider()
st.caption("CampusLoop · Built by students, for students ♻️")