# Import libraries
import streamlit as st
import pandas as pd

import altair as alt

# Set Halaman
st.set_page_config(layout='wide')

# Judul
st.title("Profil Kunjungan Wisatawan Mancanegara 2017-2022: Lebih Banyak Lewat Udara, Darat, atau Laut?")
# Nama Author
st.write("Author: Mohammad Faiz Attoriq (19mohd.faiz96@gmail.com) | [LinkedIn](https://www.linkedin.com/in/mohammad-faiz-attoriq/)")

# Menambahkan Foto
st.image('Tanah Lot.jpg', caption="Tanah Lot yang terletak di Bali menjadi salah satu destinasi wisata favorit wisatawan mancanegara di Indonesia. (Sumber: Pexels.com/Yousef Salah)", width=600)

# Pendahuluan
st.header("Pendahuluan")

# Membuat Expander Box Pendahulun
def main():

    # Buat expander
    with st.expander("Tampilkan Informasi"):
        pendahuluan = """
        Indonesia menjadi salah satu negara yang memiliki banyak destinasi wisata. Sektor perekonomian turut andil meningkatkan pendapatan negara. Pada tahun 2022, kontribusi produk domestik bruto (PDB) pariwisata Indonesia tercatat [berada di angka 3,6%](https://kemenparekraf.go.id/berita/siaran-pers-menparekraf-paparkan-penyerapan-pagu-anggaran-tahun-2022-di-hadapan-komisi-x-dpr-ri). Persentase PDB ini meningkat dari tahun lalu yang hanya berada di angka 2,4%.

        Ada 3 jenis pintu masuk untuk turis asing. Pertama, ada jalur udara berupa bandara berskala internasional yang tersebar di seluruh Indonesia. Kedua, jalur laut berupa pelabuhan internasional, mengingat negara ini berupa kepulauan yang dipisahkan oleh laut. Ketiga, karena Indonesia memiliki perbatasan negara darat, ada pintu masuk darat berupa pos perbatasan. Data dari akan ditampilkan nanti merupakan jumlah pengunjung internasional yang memiliki visa wisata.

        Analisis data profil kunjungan wisatawan mancanegara periode 2017-2022 ini memiliki 2 tujuan. Pertama, untuk mengetahui dari jalur udara, laut, dan darat, manakah yang paling sering menerima wisatawan mancanegara. Kedua, untuk mengamati bagaimana tren ketiga jenis pintu masuk tersebut selama periode data tersebut didapatkan, yaitu 2017-2019.
        """

        # Tampilkan informasi
        st.markdown(pendahuluan)

if __name__ == "__main__":
    main()

st.header("Sumber Data")
st.write(" Data yang dianalisis adalah dataset yang bersumber dari Katalog Data Kemenparekraf RI dengan judul **Jumlah Kunjungan Wisatawan Mancanegara per Bulan per Pintu Masuk 2017-2022**. Data tersebut berupa satu tabel yang berisi data tahun dari 2017 hingga 2022, nama bulan, nama pintu masuk, jenis atau jalur pintu masuk, dan jumlah kunjungan wisatawan mancanegara per nama pintu masuk. Dataset tersebut dapat diakses melalui [link berikut](https://katalogdata.kemenparekraf.go.id/dataset/jumlah-kunjungan-wisatawan-mancanegara/resource/23ef4f91-bd2b-4321-bb89-8225d9edb331).")

# Import Data dari Link CSV Spreadsheet
wisman = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vS-4IoBhE2Fn0SdsUuNAuyspbXWMbqrMhyYX4cMsTnfxv10wipMYH5Oo8po0M-muxC6kt_qXGOchWQy/pub?gid=268963969&single=true&output=csv')

# Mengganti Nama Bulan
month_dict = {
    'Januari': '01',
    'Februari': '02',
    'Maret': '03',
    'April': '04',
    'Mei': '05',
    'Juni': '06',
    'Juli': '07',
    'Agustus': '08',
    'September': '09',
    'Oktober': '10',
    'November': '11',
    'Desember': '12'
}

# Menggunakan fungsi .map() 
wisman['bulan'] = wisman['bulan'].map(month_dict)

# Membuat kolom tanggal dengan menggabungkan kolom tahun dan bulan
wisman['tanggal'] = wisman['tahun'].astype(str) + '-' + wisman['bulan']

# Konversi tipe data kolom tanggal dengan fungsi pd.to_datetime() dan .dt.date (output: format YYYY-MM-YY)
wisman['tanggal'] = pd.to_datetime(wisman['tanggal'], format='%Y-%m').dt.date

# Pengurutan berdasarkan tanggal
wisman = wisman.sort_values('tanggal')

# Pengurutan berdasarkan indeks dataframe
wisman = wisman.sort_index()

# Membuat dataframe baru: mengambil data tertentu dan kolom diurutkan
df_wisman = wisman[['tanggal', 'jenis_pintu_masuk', 'nama_pintu_masuk', 'jumlah_kunjungan']]

# Menampilkan Dataframe (Bisa comment out bila tidak diperlukan)
# df_wisman

# Profil Jenis Pintu Masuk Wisman
st.header("Profil Kunjungan Berdasarkan Jenis Pintu Masuk")

# Subheader Grafik
st.write("Grafik profil kunjungan per jenis pintu masuk")

# Agregasi Penjumlahan Masing-masing Data Jenis Pintu Masuk dan Mereset Indeks
df_chart = df_wisman.groupby(['tanggal', 'jenis_pintu_masuk']).sum().reset_index()

# Membuat Diagram Grafik
chart = alt.Chart(df_chart).mark_line().encode(
    x=alt.X('tanggal:T', axis=alt.Axis(title='Bulan')),
    y=alt.Y('jumlah_kunjungan:Q', axis=alt.Axis(title='Jumlah Kunjungan Wisman')),
    color=alt.Color('jenis_pintu_masuk:N', scale=alt.Scale(domain=['Darat', 'Laut', 'Udara'], range=['red', 'blue', 'yellow']))
).properties(
    width=alt.Step(80)
)

# Menampilkan Grafik
st.altair_chart(chart, use_container_width=True)

# Membuat Expander Box
def main():
    # Judul halaman
    st.write("Penjelasan")

    # Buat expander
    with st.expander("Tampilkan Informasi"):
        informasi = """
        Grafik di atas dapat memberikan informasi bahwa jalur udara adalah jenis pintu masuk yang paling diminati para wisatawan mancanegara. Hal ini disebabkan oleh topografi Indonesia yang berupa kepulauan. Di samping itu, jalur udara cukup membutuhkan waktu yang sangat singkat dari negara asal.
        
        Namun, jumlah kunjungan turis asing melalui jalur udara menurun tajam. Jika dari 2017 sampai Januari 2020 berkisar di antara 643.177-1.073.385, jumlah kunjungan wisatawan tersebut terjun bebas di angka 562.160 (Februari 2020), 111.323 (Maret 2020), dan anjlok di angka 783 (April 2020). Menurunnya angka tersebut diakibatkan oleh ketatnya pembatasan mobilitas sebagai respons dari merebaknya pandemi COVID-19 secara global sejak Februari 2020, kemudian masuk Indonesia pada Maret 2020.
        
        Secara umum, jalur laut memegang posisi kedua dalam tren kedatangan wisatawan mancanegara. Meskipun Indonesia dikenal sebagai negara maritim, jumlah kunjungan turis asing melalui jalur ini tidak sebanyak jalur udara, paling tinggi hanya sebanyak 388.495 kunjungan. Hal ini disebabkan oleh kurang efektifnya perjalanan laut, baik dari segi kepraktisan maupun efisiensi waktu.
        
        Dari 2017 hingga Februari 2020, angka kunjungan turis asing melalui jalur laut berkisar di angka 186.669-388.495, begitu pada Maret 2020, jumlah kedatangan turis asing melalui jalur ini merosot 111.323 dan memburuk hingga Maret 2020. Secara kasat mata, tren penurunannya sama dengan jalur udara, hanya saja tidak terlalu signifikan.
        
        Jalur darat tidak terlalu banyak diminati wisatawan mancanegara yang berkunjung ke Indonesia. Jumlah kunjungan wisatawan terbanyaknya hanya di angka 234.618 yang tercatat pada Januari 2018. Hal ini terjadi karena perjalanan ini sangat tidak efektif, belum lagi perbatasan darat Indonesia tidak terlalu panjang. Tren kedatangannya relatif lebih landai dibandingkan dengan 2 jalur kedatangan turis asing lain. Bahkan, pandemi COVID-19 tidak berpengaruh apa-apa terhadap tren tersebut.
        
        Kabar baiknya, baik jalur udara maupun laut sama-sama mengalami tren positif sejak Februari 2022. Hal ini bisa terjadi karena adanya pelonggaran aturan kedatangan internasional, termasuk wisatawan mancanegara. Pintu kedatangan melalui jalur udara kembali ke tren sebelum COVID-19, lebih kuat kenaikannya jika dibandingkan dengan 2 jalur lainnya. Begitu pula dengan jalur laut yang mengalami tren positif kembali meskipun masih lemah daripada sebelum pandemi tersebut.
        
        Secara keseluruhan, dapat disimpulkan bahwa 3 tahun selama pandemi COVID-19 mengalami kemerosotan jumlah kunjungan wisatawan mancanegara yang lebih tajam daripada tahun-tahun sebelum wabah tersebut. Pembatasan mobilitas dan kebijakan Indonesia maupun luar negeri sangat memegang andil dalam turunnya jumlah kunjungan tersebut. Tentunya, itu semua untuk menekan penularan wabah tersebut.

        """

        # Tampilkan informasi
        st.markdown(informasi)

if __name__ == "__main__":
    main()

# Profil Jenis Pintu Masuk Wisman
st.header("Pintu Masuk Mana yang Paling Banyak Dikunjungi?")

# Membuat Select Box untuk Memilih Jenis Pintu Masuk
jenis_pintu_masuk_options = ['Semua', 'Udara', 'Laut', 'Darat']
selected_jenis_pintu_masuk = st.selectbox('Pilih Jenis Pintu Masuk', jenis_pintu_masuk_options)

# Membuat Select Box untuk Memilih Tahun
time_options = ['Semua (2017-2022)', '2017', '2018', '2019', '2020', '2021', '2022']
selected_time = st.selectbox('Pilih Tahun', time_options)

# Fungsi Filter Data untu Pintu Masuk dan Waktu (Tahun)
if selected_time == 'Semua (2017-2022)' and selected_jenis_pintu_masuk == 'Semua':
    filtered_data = df_wisman
elif selected_time == 'Semua (2017-2022)':
    filtered_data = df_wisman[df_wisman['jenis_pintu_masuk'] == selected_jenis_pintu_masuk]
elif selected_jenis_pintu_masuk == 'Semua':
    filtered_data = df_wisman[(pd.to_datetime(df_wisman['tanggal']).dt.year == int(selected_time))]
else:
    filtered_data = df_wisman[(df_wisman['jenis_pintu_masuk'] == selected_jenis_pintu_masuk) & (pd.to_datetime(df_wisman['tanggal']).dt.year == int(selected_time))]

# (1) Fungsi Group by untuk Mengelompokkan Data Nama Pintu Masuk
# (2) Fungsi Agregat Jumlah Kunjungan Tiap Nama Pintu Masuk
bar_chart_data = filtered_data.groupby('nama_pintu_masuk')['jumlah_kunjungan'].sum().reset_index()

# Mengurutkan Jenis Pintu Masuk Berdasarkan Jumlah Kunjungan
bar_chart_data = bar_chart_data.sort_values('jumlah_kunjungan', ascending=False)

# Membuat Diagram Batang (Bar Chart) Horizontal
bar_chart = alt.Chart(bar_chart_data).mark_bar().encode(
    y=alt.Y('nama_pintu_masuk:N', sort='-x'),
    x='jumlah_kunjungan:Q',
    color=alt.Color('nama_pintu_masuk:N', scale=alt.Scale(scheme='category20'), legend=None),
    tooltip=['nama_pintu_masuk:N', 'jumlah_kunjungan:Q']
).properties(
    width=alt.Step(80)
)

# Menampilkan Diagram Horizontal
st.altair_chart(bar_chart, use_container_width=True)

# Penjelasan
def main():
    # Judul halaman
    st.write("Penjelasan")

    # Pilihan untuk select box
    pilihan = ["Pilih di sini" ,"Udara", "Laut", "Darat"]

    # Buat select box
    selected_option = st.selectbox("Pilih informasi:", pilihan)

    # Tampilkan informasi sesuai dengan pilihan
    if selected_option == "Udara":
        informasi = """
        Jalur udara merupakan pintu masuk terbanyak yang dikunjungi wisatawan mancanegara selama periode 2017-2022. Bandara-bandara tersebut antara lain Adi Sucipto (Yogyakarta), Ahmad Yani (Semarang-Jateng), Bandara Internasional Lombok (lombok Tengah-NTB), Hasanuddin (MakassarSulsel), Husein Sastranegara (Bandung-Jabar), Juanda (dekat Surabaya-Jatim), Kualanamu (Deli Serdang-Sumut), Minangkabau (Padang Pariaman-Sumbar), Ngurah Rai (dekat Denpasar-Bali), Sam Ratulangi (Manado-Sulut), Soekarno-Hatta (Tangerang-banten), Sultan Badaruddin II (Palembang-Sulsel), Sultan Iskandar Muda (Aceh), Sultan Syarif Kasim II (Pekanbaru-Riau), dan Supadio (dekat Pontianak-Kalbar). Ada pun bandara selain yang tertera di dataset diberi keterangan Pintu Udara Lainnya.

        Selama periode dataset tersebut diambil, bandara yang yang paling sering menerima turis asing adalah Bandara Ngurah Rai sebanyak 21.160.837 kedatangan. Jumlah ini kurang lebih 2 kali lebih banyak daripada jumlah kedatangan turis yang melalui Bandara Soekarno-Hatta, yaitu sebanyak 9.471.966 kunjungan. Banyaknya wisatawan mancanegara berkunjung ke bandara tersebut disebabkan oleh Bali yang sudah dikenal sejak lama sebagai destinasi wisata, seperti Tanah Lot, Kuta, Sanur, Lovina, Tanjung Benoa, Uluwatu, Ubud, dan masih banyak lagi.

        Bandara Ngurah Rai kerap memegang posisi pertama pintu masuk udara selama periode tersebut, kecuali pada tahun 2021 menyusut dan berganti menjadi Bandara Soekarno-Hatta. Dalam tahun yang sama, sudah 119.063 turis asing yang mendarat di Bandara Soekarno-Hatta, sementara Ngurah Rai tercatat hanya menerima 43 kunjungan. Bergantinya tren ini berkaitan dengan pembatasan mobilitas imbas wabah COVID-19. Kebijakan dalam negeri membuat hampir semua penerbangan dialihkan ke bandara yang masih terbilang dekat dengan ibu kota negara. Ketika aturan bepergian mulai longgar pada tahun 2022, Bandara Ngurah Rai kembali menempati posisi puncak kedatangan wisatawan mancanegara dengan total kunjungan sebanyak 2.154.045, jauh mengungguli Bandara Soekarno-Hatta yang meraup 934.661 turis asing.
        """
    elif selected_option == "Laut":
        informasi = """
        Meskipun udara menjadi jalur masuk Indonesia favorit, jalur laut cukup banyak digunakan oleh wisatawan asing. Dalam data Kemenparekraf RI, pelabuhan yang tercatat antara lain Batam, Tanjung Balai Karimun, Tanjung Pinang, dan Tanjung Uban (Kepri), Tanjung Mas (Semarang-Jateng), dan Tanjung Benoa (Bali). Ada pun berbagai pintu masuk laut lainnya tercatat sebagai Pintu Laut Lainnya.

        Selama periode 2017-2022 secara keseluruhan, Batam menjadi pelabuhan yang paling banyak menerima turis asing dari jalur laut yaitu sebanyak 6.260.782. Ini bisa terjadi karena lokasi Batam yang sangat strategis: dekat dengan Singapura dan perairannya sering dilintasi kapal-kapal internasional. Batam dikenal dengan destinasi wisata bahari dengan berbagai pantai, seperti Pulau Abang, Pantai Nongsa, Pulau Belakang Padang, pantai Ocarina, dan spot foto seperti Jembatan Barelang. Ada pun monumen bertuliskan Welcome to Batam menjadi primadona wisatawan.

        Namun, sejak pandemi COVID-19 melanda pada tahun 2020, tren kedatangan Batam hanya menerima 286.336 wisatawan asing. 2021 menjadi tahun terparah bagi pelabuhan tersebut karena hanya menerima 2.582 kunjungan. Meskipun begitu, posisi Batam sebagai juara pertama jumlah kedatangan wisatawan luar negeri tidak tergantikan (dengan mengabaikan kategori Pintu Laut Lainnya.)
        """
    elif selected_option == "Darat":
        informasi = """
        Karena memiliki perbatasan darat, Indonesia memiliki pintu masuk wisatawan mancanegara berupa Pos Lintas Batas Negara (PLBN). Data yang disajikan untuk jalur darat ini antara lain Entikong (Sanggau-Kalbar), Aruk (Sambas-Kalbar), dan Nanga Badau (Kapuas Hulu-Kalbar) untuk perbatasan dengan Malaysia, Atambua atau dikenal dengan PLBN Motaain (Belu-NTT) untuk perbatasan dengan Timor Leste, dan Jayapura atau dikenal dengan PLBN Skouw (Papua). Sementara pintu perbatasan lain yang tidak termasuk dalam data tersebut tercatat sebagai Pintu Darat Lain.
        
        Selama periode 2017-2022, wisatawan mancanegara paling sering lewat Atambua sebanyak 299.247 kunjungan, lalu disusul oleh Jayapura sebanyak 291.556 turis asing. Namun, jika meliha data per tahun, mulanya Jayapura yang mendominasi pada tahun 2017 dan 2018. Begitu sejak 2019 sampai 2022, posisi pemuncak pada data tersebut diduduki oleh Atambua. Ada kemungkinan banyaknya destinasi wisata di NTT secara keseluruhan (Taman Nasional Komodo, Kampung Wae Rebo, dan berbagai pantai di kawasan Kupang) menjadi faktornya.

        Tidak seperti jalur udara maupun laut, jalur darat sangat sedikit diminaati. Hal ini terjadi karena WNA yang melintasi pintu perbatasan tersebut tidak banyak untuk berwisata, melainkan untuk bekerja. Kalau pun ada, itu dari selain negara perbatasan darat, seperti WNA yang melakukan perjalanan darat dan memasuki Indonesia.
        """
    else:
        informasi = """
        Silakan memilih informasi telebih dahulu untuk menampilkan salah satu informasi.
        """

    # Tampilkan informasi
    st.markdown(informasi)

if __name__ == "__main__":
    main()

# Kesimpulan
def main():
    # Header
    st.header("Kesimpulan")

    # Buat expander
    with st.expander("Tampilkan Informasi"):
        kesimpulan = """
        Dari analisis data di atas, dapat ditarik kesimpulan:

        1. Jalur udara menjadi pintu masuk yang paling sering dikunjungi wisatawan mancanegara, kecuali pada tahun 2021.

        2. Selama periode 2017 sampai Januari 2020, tren kedatangan wisatawan mancanegara cukup positif, tetapi mengalami tren negatif sejak Februari 2020 sampai tren menguat kembali pada Februari 2022.
        """

        # Tampilkan informasi
        st.markdown(kesimpulan)

if __name__ == "__main__":
    main()