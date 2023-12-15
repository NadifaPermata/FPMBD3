import streamlit as st
from sqlalchemy import text

list_petugas = ['', 'Nuryanto', 'Angel', 'Siola', 'Riki', 'Karan']
list_bbm = ['', 'pertalite', 'pertamax', 'pertamax turbo', 'solar', 'pertamina dex']

#Add a heading for the company with a logo
company_name = "PT Pertamina Indonesia"  # Replace with the actual name of your company
st.title(company_name)

# Add a logo
company_logo_url = "https://solusiprinting.com/wp-content/uploads/2023/02/Solusi-Printing-Logo-Pertamina-Baru-1280-x-720-pixel-1024x576.jpg"  # Replace with the URL of your company logo
st.image(company_logo_url, caption=company_name, use_column_width=True, width=50)

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://NadifaPermata:7CIXwskWNRy0@ep-falling-cherry-06864175.us-east-2.aws.neon.tech/mbd3")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS SELLING (id serial, nama_petugas varchar, plat_nomor char(25), jenis_kendaraan varchar, \
                                                       bbm text, banyak_pembelian integer, tanggal date);')
    session.execute(query)

st.write(
    f"""
    <style>
        .stApp {{
            background-color: #99FFFF;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.header('DATABASE PENGUNJUNG SPBU WILAYAH KOTA SURABAYA')
page = st.sidebar.selectbox("Pilih Menu", ["View Data", "Edit Data"])

if page == "View Data":
    # Retrieve data from the database
    data = conn.query('SELECT * FROM selling where waktu is not null ORDER By id;', ttl="0").set_index('id')

    # Add a search bar
    search_query = st.text_input("Search by plat_nomor:", "")
    filtered_data = data[data['plat_nomor'].str.contains(search_query, case=False, na=False)]
    st.dataframe(filtered_data)
    
if page == "Edit Data":
    if st.form('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO selling (nama_petugas, plat_nomor, jenis_kendaraan, bbm, banyak_pembelian, waktu, tanggal) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'', '5':'', '6':None, '7':None})
            session.commit()

    data = conn.query('SELECT * FROM selling where waktu is not null ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_petugas_lama = result["nama_petugas"]
        plat_nomor_lama = result["plat_nomor"]
        jenis_kendaraan_lama = result["jenis_kendaraan"]
        bbm_lama = result["bbm"]
        banyak_pembelian_lama = 0
        waktu_lama = result["waktu"]
        tanggal_lama = result["tanggal"]

        with st.expander(f'{plat_nomor_lama}'):
            with st.form(f'data-{id}'):
                nama_petugas_baru = st.selectbox("nama_petugas", list_petugas, list_petugas.index(nama_petugas_lama))
                plat_nomor_baru = st.text_input("plat_nomor", plat_nomor_lama)
                jenis_kendaraan_baru = st.text_input("jenis_kendaraan", jenis_kendaraan_lama)
                bbm_baru = st.selectbox("bbm", list_bbm, list_bbm.index(bbm_lama))
                banyak_pembelian_baru = st.number_input("Masukkan banyak pembelian (baru)", value=banyak_pembelian_lama, step=1)
                waktu_baru = st.time_input("waktu", waktu_lama)
                tanggal_baru = st.date_input("tanggal", tanggal_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE selling \
                                          SET nama_petugas=:1, plat_nomor=:2, bbm=:3, jenis_kendaraan=:4, \
                                          banyak_pembelian=:5, waktu=:6, tanggal=:7 \
                                          WHERE id=8;')
                            session.execute(query, {'1':nama_petugas_baru, '2':plat_nomor_baru, '3':(bbm_baru), '4':jenis_kendaraan_baru, 
                            '5':banyak_pembelian_baru, '6':waktu_baru, '7':tanggal_baru, '8':id})
                            session.commit()
                            st.experimental_rerun()
                            st.success("Data updated successfully!")
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM selling WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()