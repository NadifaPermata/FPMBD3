import streamlit as st
from sqlalchemy import text

list_petugas = ['', 'Nuryanto', 'Angel', 'Siola', 'Riki', 'Karan']
list_bbm = ['', 'pertalite', 'pertamax', 'pertamax turbo', 'solar', 'pertamina dex']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://NadifaPermata:7CIXwskWNRy0@ep-falling-cherry-06864175.us-east-2.aws.neon.tech/mbd3")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS SELLING (id serial, nama_petugas varchar, plat_nomor char(25), jenis_kendaraan varchar, \
                                                       bbm text, banyak_pembelian char(2), tanggal date);')
    session.execute(query)

st.header('SPBU DATA MANAGEMENT')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM selling ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.form('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO selling (nama_petugas, plat_nomor, jenis_kendaraan, bbm, banyak_pembelian, waktu, tanggal) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'', '5':'', '6':None, '7':None})
            session.commit()

    data = conn.query('SELECT * FROM selling ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_petugas_lama = result["nama_petugas"]
        plat_nomor_lama = result["plat_nomor"]
        jenis_kendaraan_lama = result["jenis_kendaraan"]
        bbm_lama = result["bbm"]
        banyak_pembelian_lama = result["banyak_pembelian"]
        waktu_lama = result["waktu"]
        tanggal_lama = result["tanggal"]

        with st.expander(f'{plat_nomor_lama}'):
            with st.form(f'data-{id}'):
                nama_petugas_baru = st.selectbox("nama_petugas", list_petugas, list_petugas.index(nama_petugas_lama))
                plat_nomor_baru = st.text_input("plat_nomor", plat_nomor_lama)
                jenis_kendaraan_baru = st.text_input("jenis_kendaraan", jenis_kendaraan_lama)
                bbm_baru = st.selectbox("bbm", list_bbm, list_bbm.index(bbm_lama))
                banyak_pembelian_baru = st.text_input("banyak_pembelian (dalam_liter)", banyak_pembelian_lama)
                waktu_baru = st.time_input("waktu", waktu_lama)
                tanggal_baru = st.date_input("tanggal", tanggal_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE selling \
                                          SET nama_petugas=:1, plat_nomor=:2, symptom=:3, jenis_kendaraan=:4 \
                                          banyak_pembelian=:5, waktu=:6, tanggal=:7 \
                                          WHERE id=:7;')
                            session.execute(query, {'1':nama_petugas_baru, '2':plat_nomor_baru, '3':(bbm_baru), '4':jenis_kendaraan_baru, 
                            '5':banyak_pembelian_baru, '6':waktu_baru, '7':tanggal_baru, '8':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM selling WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()