// ---------- HELPER NODES --------------
// Parliament
MERGE (DPR:Parliament {
        index:'DPR',
        name:'Dewan Perwakilan Rakyat',
        alias:'DPR',
        description:'2019-2024 Indonesian Parliament',
        period_start_year:2019,
        period_end_year:2024,
        total_seat:575
    }
)

// Ideologies and Political Leanings
MERGE (Pancasila:Principle {
        index:'Pancasila',
        name:'Pancasila', 
        description:'Not pursuing to promote Islam in government and law'
    }
)
MERGE (Islamic_religious:Principle {
        index:'Islamic_religious',
        name:'Pancasila and Islam', 
        description:'promoting islamic value in government and law'
    }
)

MERGE (Progressive:Political_Leaning {
        index:'Progressive',
        name:'Progressive', 
        description:'Supporting progressive value and more readily embrace change'
    }
)
MERGE (Conservative:Political_Leaning {
        index:'Conservative',
        name:'Conservative', 
        description:'Supporting conservative/traditional value'
    }
)
MERGE (Regulated_Economy:Economic_view {
        index:'Regulated_Economy',
        name:'Regulated Economy', 
        description:'Supporting stronger government involvement in economy with the aim of achieving economic equality'
    }
)
MERGE (Liberal_Economy:Economic_view {
        index:'Liberal_Economy',
        name:'Liberal Economy', 
        description:'Supporting less government involvement in economy with the aim of achieving high economic growth'
    }
)

// Geography
MERGE (Indonesia:Country {
        index:'Indonesia',
        name:'Indonesia', 
        independence_date:'17 August 1997'
})
MERGE (Gorontalo:RegionVote {
        index:'Gorontalo',
        name:'Gorontalo'
})
MERGE (Jambi:RegionVote {
        index:'Jambi',
        name:'Jambi'})
MERGE (Sumsel:RegionVote {
        index:'Sumsel',
        name:'Sumatera Selatan'})

// Office Position
MERGE (MenteriKoordinatorEkonomi:OfficePosition {
        index:'MenteriKoordinatorEkonomi',
        name:'Menteri Koordinator Bidang Perekonomian'
    }
)
MERGE (MenteriKoordinatorMaritim:OfficePosition {
        index:'MenteriKoordinatorMaritim',
        name:'Menteri Koordinator Bidang Kemaritiman dan Investasi'
    }
)
MERGE (KepalaStafPresiden:OfficePosition {
        index:'KepalaStafPresiden',
        name:'Kepala Staf Kepresidenan Republik Indonesia'
    }
)
MERGE (MenteriKoordinatorPolitikHukumKeamanan:OfficePosition {
        index:'MenteriKoordinatorPolitikHukumKeamanan',
        name:'Menteri Koordinator Bidang Politik, Hukum, dan Keamanan'
    }
)
MERGE (MenteriESDM:OfficePosition {
        index:'MenteriESDM',
        name:'Menteri Energi dan Sumber Daya Mineral'
    }
)
MERGE (MenteriPemudaDanOlahraga:OfficePosition {
        index:'MenteriPemudaDanOlahraga',
        name:'Menteri Pemuda dan Olahraga'
    }
)
MERGE (MenteriSosial:OfficePosition {
        index:'MenteriSosial',
        name:'Menteri Sosial'
    }
)
MERGE (MenteriPerindustrian:OfficePosition {
        index:'MenteriPerindustrian',
        name:'Menteri Perindustrian'
    }
)

// Jenis Kasus
MERGE (Gratifikasi:JenisKasus {
    index:'Gratifikasi',
        name:'Suap dan Gratifikasi',
    description:'suap dapat didefinisikan sebagai memberi atau menerima hadiah (uang, barang, jasa) atau janji, karena kewenangan/kekuasaan jabatan penerima atau dengan maksud agar yang menerima berbuat/tidak berbuat sesuatu yang berlawanan dengan kewajiban, atau sebagai imbalan. Sementara gratifikasi dapat didefinisikan sebagai pemberian dalam arti luas (bisa uang, barang, diskon, fasilitas, dll.) tanpa janji. Gratifikasi bisa dianggap suap bagi penyelenggara negara jika berhubungan dengan jabatannya dan berlawanan dengan kewajibannya (dan tidak dilaporkan ke KPK per pasal 12C UU Tipikor)'
})
MERGE (Korupsi:JenisKasus {
    index:'Korupsi',
        name:'Kerugian Keuangan Negara',
    description:'Jumlah berkurangnya atau hilangnya kekayaan dan hak Negara (uang, surat berharga, barang) akibat tindakan pidana korupsi yang dilakukan.'
})

// ------- BASE BIJAK MEMILIH NODES ---------
// ---- Law
MERGE (UU_IKN:Law {
    index:'UU_IKN',
    name:'UU Ibukota Negara / UU IKN',
    formal_name:'Undang-undang (UU) Nomor 3 Tahun 2022',
    isInEffect:True,
    description:'UU ini mengatur mengenai Ibu Kota Nusantara dan pelaksanaan pemerintahannya yang dilaksanakan oleh Otorita Ibu Kota Nusantara.',
    source:'https://peraturan.bpk.go.id/Details/198400/uu-no-3-tahun-2022'
})
MERGE (PerppuCiptaker:Law {
    index:'PerppuCiptaker',
    name:'Perppu Ciptaker',
    formal_name:'Peraturan Pemerintah Pengganti Undang-Undang (Perppu) No. 2 Tahun 2022 tentang Cipta Kerja',
    isInEffect:True,
    description:'Ruang lingkup Peraturan Pemerintah Pengganti Undang-Undang tentang Cipta Kerja ini meliputi: 1. peningkatan ekosistem investasi dan kegiatan berusaha; 2. ketenagakerjaan; 3. kemudahan, pelindungan, serta pemberdayaan Koperasi dan UMK-M; 4. kemudahan berusaha; 5. dukungan riset dan inovasi; 6. pengadaan tanah; 7. kawasan ekonomi; 8. investasi Pemerintah Pusat dan percepatan proyek strategis nasional; 9. pelaksanaan administrasi pemerintahan; dan 10. pengenaan sanksi.',
    source:'https://peraturan.bpk.go.id/Details/234926/perpu-no-2-tahun-2022'
}) 
MERGE (UU_Ciptaker:Law {
    index:'UU_Ciptaker',
    name:'UU Cipta Kerja',
    formal_name:'Undang-undang (UU) Nomor 11 Tahun 2020 tentang Cipta Kerja',
    isInEffect:True,
    description:'UU ini mengatur mengenai upaya cipta kerja yang diharapkan mampu menyerap tenaga kerja Indonesia yang seluas-luasnya di tengah persaingan yang semakin kompetitif dan tuntutan globalisasi ekonomi. Cipta Kerja adalah upaya penciptaan kerja melalui usaha kemudahan, perlindungan, dan pemberdayaan koperasi dan usaha mikro, kecil, dan menengah, peningkatan ekosistem investasi dan kemudahan berusaha, dan investasi Pemerintah Pusat dan percepatan proyek strategis nasional. Sepuluh ruang lingkup UU ini adalah: 1. peningkatan ekosistem investasi dan kegiatan berusaha; 2. ketenagakerjaan; 3. kemudahan, perlindungan, serta pemberdayaan Koperasi dan UMK-M; 4. kemudahan berusaha; 5. dukungan riset dan inovasi; 6. pengadaan tanah; 7. kawasan ekonomi; 8. investasi Pemerintah Pusat dan percepatan proyek strategis nasional; 9. pelaksanaan administrasi pemerintahan; dan 10. pengenaan sanksi.',
    source:'https://peraturan.bpk.go.id/Details/234926/perpu-no-2-tahun-2022'
})

MERGE (UU_EBT:Law {
    index:'UU_EBT',
    name:'UU Energi Baru dan Energi Terbarukan / UU EB-ET',
    formal_name:'',
    isInEffect:False,
    description:'UU ini mengatur dirancang untuk mendorong peningkatan target iklim dan mengurangi emisi gas rumah kaca Indonesia.Utamanya dengan penggantian energi fosil dengan energi baru dan terbarukan. salah satu poin yg dijadikan perdebatan adalah masuknya energi baru berbasis batubara yang dianggap tidak lebih baik dari batubara dalam hal emisi gas rumah kaca',
    source:''
})
MERGE (KUHP:Law {
    index:'KUHP',
    name:'UU Kitab Undang-Undang Hukum Pidana',
    formal_name:'Undang-undang (UU) Nomor 1 Tahun 2023 tentang Kitab Undang-Undang Hukum Pidana',
    isInEffect:True,
    description:'UU ini mengatur mengenai Kitab Undang-undang Hukum Pidana (KUHP). UU ini berisi Buku Kesatu dan Buku Kedua. Buku Kesatu UU ini Buku Kesatu berisi aturan umum sebagai pedoman bagi penerapan Buku Kedua serta Undang-Undang di luar Undang-Undang ini, Peraturan Daerah Provinsi, dan Peraturan Daerah kabupaten/Kota, kecuali ditentukan lain menurut Undang-Undang sehingga Buku Kesatu juga menjadi dasar bagi Undang-Undang di luar Undang-Undang ini. ',
    source:'https://peraturan.bpk.go.id/Details/234935/uu-no-1-tahun-2023'
})
MERGE (UU_KPK:Law {
    index:'UU_KPK',
    name:'UU Komisi Pemberantasan Tindak Pidana Korupsi',
    formal_name:'Undang-undang (UU) Nomor 30 Tahun 2002 tentang Komisi Pemberantasan Tindak Pidana Korupsi',
    isInEffect:True,
    description:'UU ini mengatur tugas, wewenang, dan tata cara kerja Komisi Pemberantasan Tindak Pidana Korupsi (KPK)',
    source:'https://peraturan.bpk.go.id/Details/44493/uu-no-30-tahun-2002'
})
MERGE (UU_ITE:Law {
    index:'UU_ITE',
    name:'Revisi Undang-undang Informasi Dan Transaksi Elektronik (ITE)',
    formal_name:'',
    isInEffect:False,
    description:'Membahas RKUHP & merevisi UU ITE untuk menghilangkan pasal karet alias pasal yang penafsirannya dapat berbeda-beda dan mudah sekali untuk diinterpretasikan secara sepihak',
    source:''
})
MERGE (UU_Cukai:Law {
    index:'UU_Cukai',
    name:'UU Cukai',
    formal_name:'',
    isInEffect:False,
    description:'Undang-undang ini mengatur kenaikan cukai atau pajak untuk beberapa jenis barang konsumsi seperti rokok dan minuman berpemanis. hal ini diharapkan untuk meningkatkan kesehatan rakyat dan mengurangi beban anggaran kesehatan seperti BPJS',
    source:''
})

MERGE (RUU_Adat:Law {
    index:'RUU_Adat',
    name:'RUU Masyarakat Hukum Adat',
    formal_name:'',
    isInEffect:False,
    description:'Rancangan Undang-Undang (RUU) Cipta Kerja yang memiliki beberapa pasal untuk mempermudah investasi agar dapat membuat banyak lapangan kerja, ternyata kemungkinan menjadi bumerang buat hak-hak masyarakat adat',
    source:''
})
// ---- Issue
MERGE (IbukotaNegara:Issue {
    index:'IbukotaNegara',
    name:'Ibukota Negara Baru',
    description:'Pemindahan Ibukota Negara dari Jakarta ke Kalimantan Timur dan pembentukan Otorita IKN sebagai penyelenggara pemerintahan di ibukota baru. Pembangunan IKN Nusantara ini juga diklaim sejalan dengan beberapa prioritas pemerintah lainnya, seperti mengembangkan ekonomi yang ramah lingkungan, mencapai emisi net zero pada 2060, serta visi Presiden Jokowi mewujudkan Visi Indonesia 2045'

})
MERGE (HakAdat:Issue {
    index:'HakAdat',
    name:'Hak Masyarakat Adat',
    description:'Sebagai warga negara Indonesia, masyarakat adat punya hak atas tanah, kegiatan ekonomi, dan hak sosial. Tapi,  Rancangan Undang-Undang (RUU) Cipta Kerja yang memiliki beberapa pasal untuk mempermudah investasi agar dapat membuat banyak lapangan kerja, ternyata kemungkinan menjadi bumerang buat hak-hak masyarakat adat. Aliansi Masyarakat Adat Nusantara (AMAN) bilang kalau UU Ciptaker ini malah buka jalan bagi perusahaan besar untuk menggencarkan usaha dan pengelolaan sumber daya alam. Masalahnya, hal ini bisa merugikan masyarakat adat yang punya hubungan khusus dengan tanah dan hutan sebagai tempat tinggal dan sumber penghidupan. Apalagi, masyarakat adat nggak diajak ngobrol sama sekali selama proses RUU Ciptaker, padahal mereka kan yang paling kena dampaknya. Nah, adanya perbedaan kepentingan antara investor dan masyarakat adat semakin menunjukkan adanya dilema pemerintah dalam pengesahan RUU masyarakat adat. '

})
MERGE (TransisiEnergi:Issue {
    index:'TransisiEnergi',
    name:'Transisi Energi untuk target iklim',
    description:'Pada September 2022, Presiden Jokowi menetapkan peningkatan target iklim untuk Indonesia, loh. Kalau pakai skenario kemampuan kita sendiri, emisi yang dikurangi bisa sebesar 31,8%. Kalau ada bantuan internasional, target pengurangannya bisa hingga 43,2%. Sejalan dengan ini, pemerintah meningkatkan target untuk mengurangi emisi gas rumah kaca di sektor energi hingga 358 MTCO2e (metrik ton karbon dioksida ekuivalen). Nah, salah satu cara untuk mencapai target itu adalah dengan mengganti energi berbasis fosil (batu bara dan BBM) ke energi baru dan terbarukan (surya, air, dll.). Saat ini, pemerintah baru memakai 0,3%, atau sekitar 12,4 GW, dari total potensi yang kita punya. Sedangkan target nasional tahun 2025 itu sebesar 23% campuran energi baru terbarukan. Saat ini, pemerintah lagi mendorong Rancangan Undang Undang Energi Baru dan Energi Terbarukan (RUU EB-ET). Tapi, rancangan tersebut banyak yang kurang setuju nih. Yang tadinya mendorong energi terbarukan seperti tenaga surya atau air, RUU EB-ET malah memasukan produk turunan batubara yang justru bisa menghambat penurunan emisi seperti batubara tergaskan, batubara tercairkan, dan gas metana batubara sebagai sumber energi baru. Di bulan November 2022, Komisi VII DPR, yang memimpin pengesahan RUU ini, sudah dapat rancangan Daftar Inventarisasi Masalah (DIM) dari Kementerian ESDM dan lagi menunggu penyerahan DIM final dari Sekretariat Negara. Sugeng Suparwoto, Ketua Komisi VII DPR RI, mengatakan salah satu hal yang jadi tantangan pengesahan RUU ini adalah politik fosil, di mana banyak tokoh politik besar di Indonesia yang punya bisnis komoditas batu bara. Tantangan lainnya adalah usulan pemerintah untuk masukin ketentuan power wheeling, yaitu pemakaian bersama jaringan tenaga listrik yang memperbolehkan swasta untuk menjual listrik ke masyarakat. Power wheeling ini dianggap melanggar konstitusi karena penyediaan listrik berdampak terhadap kebutuhan hidup banyak orang, makanya harus dikuasai sama negara.'

})
MERGE (Cukai:Issue {
    index:'Cukai',
    name:'Cukai Rokok dan Minuman Berpemanis',
    description:'Sampai saat ini, proses perumusan UU Cukai, atau pungutan pajak yang dikelola oleh negara yang dikenakan terhadap barang-barang tertentu, masih belum diterapkan. Niatan pemerintah buat menaikan tarif cukai adalah karena meningkatnya kasus penyakit jantung, stroke dan kanker yang disebabkan oleh rokok. Tapi ga heran, rencana ini justru banyak ditentang oleh pihak pengusaha dan petani tembakau. Apalagi, sebanyak 5.98 juta orang yang bekerja di industri tembakau bisa terkena imbasnya. Selain itu, pemerintah juga lagi membuat tarif cukai minuman manis. Alasannya juga demi kesehatan, terutama karena tingginya angka penderita diabetes di Indonesia yang mencapai 19,4 juta orang di tahun 2021.  Kalau cukai minuman manis ini diterapkan, harga minuman manis bakal menjadi lebih mahal. Orang-orang sekarang harus beneran mikir dulu sebelum membeli minum-minuman manis yang selama 20 tahun terakhir sudah naik konsumsinya sampai 15 kali lipat lho… Menteri Keuangan Sri Mulyani juga mengatakan kalau cukai minuman manis ini bisa menambah pemasukan negara dan mengurangi beban anggaran kesehatan seperti BPJS. Tapi, Bea Cukai Kementerian Keuangan bilang penerapan cukai ini harus ditunda dulu karena masalah ekonomi dan dampaknya yang besar ke tenaga kerja. Jadi, penerapan cukai ini kelihatannya sih maju-mundur karena beberapa efek domino yang buat pemerintah harus mikir keras buat cari solusi seimbang yang harapanya engga membebani masayarakat.'
})
MERGE (FreedomOfSpeech:Issue {
    index:'FreedomOfSpeech',
    name:'Kebebasan Berpendapat',
    description:'Kita bisa mengukur kesehatan demokrasi sebuah bangsa dengan melihat kebebasan warganya dalam menyampaikan pendapat. Sayangnya, dari hasil Survei Nasional 2022, lebih dari 60% masyarakat Indonesia merasa tidak bebas dan bahkan takut untuk mengekspresikan pendapat mereka. Saat ini, Undang-Undang Nomor 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik (UU ITE) adalah UU yang mengatur aktivitas dan informasi online, platform media sosial, serta hukum kejahatan siber.Akhir-akhir ini, UU ITE sering dipakai oleh pihak yang memiliki kekuasaan untuk mengkriminalisasi, atau mengancam untuk mengkriminalisasi, beberapa opini atau kritikan terhadap mereka dan/atau pemerintah. Sejak tahun 2021, usulan untuk merevisi UU ITE sudah sering dibahas, namun rancangan revisinya belum ada sampai sekarang. Nah, penghapusan pasal karet tadi jadi salah satu faktor penting dari rencana revisi UU ITE ini. Sebenernya sejak Juni 2021 lalu, pemerintah, melalui Kementerian Komunikasi dan Informatika (Kemenkominfo), sudah menyiapkan buku pedoman untuk mengartikan UU ITE. Tujuannya tentu saja supaya bisa mencegah penerapan pasal karet. Namun, upaya ini dinilai belum cukup oleh masyarakat sipil, dan hingga saat ini buku pedoman tersebut belum diterbitkan. Kebebasan menyampaikan pendapat juga menjadi isu dalam Rancangan Kitab Undang-Undang Hukum Pidana (RKUHP). Memang benar, RKUHP telah memberi pengecualian bahwa informasi yang berkepentingan publik tidak lagi termasuk dalam pencemaran nama baik. Tapi, pasal di RKUHP tetap berpotensi untuk disalahgunakan dan membatasi kebebasan berpendapat melalui pasal-pasal yang berkaitan dengan mengkritik presiden (pasal 218) ataupun institusi pemerintah (pasal 240).'
})
MERGE (EradicatingCorruption:Issue {
    index:'EradicatingCorruption',
    name:'Keseriusan Pemberantasan Korupsi',
    description:'Engga bisa dipungkiri kalau korupsi itu salah satu masalah yang paling mengakar dan mendesak di Indonesia. Nah, kita sebagai masyarakat bisa mengukur komitmen pemerintah untuk memberantas korupsi secara institusional melalui Komisi Pemberantasan Korupsi (KPK) sebagai lembaga utama yang bertugas memberantas korupsi. Salah satu kontroversi politik terbesar terkait korupsi dan KPK adalah revisi UU KPK (UU No.30/2002) di tahun 2019 (UU No.19/2019). Beberapa organisasi masyarakat, koalisi, akademisi, dan aktivis menganggap revisi ini sebagai cara untuk melemahkan KPK. Sementara itu, pihak DPR membantah tuduhan ini. Revisi ini juga menjadi pemicu demonstrasi besar-besaran dengan tagar #ReformasiDikorupsi. Banyak banget alasan mengapa revisi UU KPK dianggap melemahkan KPK, tetapi salah satu yang paling signifikan adalah pembentukan Dewan Pengawas KPK (Dewas) yang dianggap membatasi dan menghambat langkah-langkah penyidik KPK. Aturan kontroversial dalam UU tersebut adalah perubahan status pegawai KPK menjadi PNS yang dianggap bisa menghambat independensi pegawai dalam memproses kasus. Kamu bisa baca Revisi UU KPK di sini. Ditambah lagi, pada tahun 2019 Firli Bahuri dipilih sebagai Ketua KPK oleh Komisi III DPR. Masalahnya, Firli telah beberapa kali terbukti melanggar kode etik dan memiliki catatan kerja yang kurang baik. Hal ini juga dianggap sebagai upaya lain untuk melemahkan KPK dalam memberantas korupsi.'
})

MERGE (SexEducation:Issue {
    index:'SexEducation',
    name:'Pendidikan Kesehatan Reproduksi',
    description:'Pendidikan kesehatan seksual dan reproduksi tuh memang hal yang masih tabu di masyarakat kita. Tapi bukan berarti hal ini enggak penting untuk dipelajari demi kesehatan kita semua. Soalnya, kesehatan seksual dan reproduksi yang baik bisa memberi peluang untuk ningkatin kualitas hidup dan potensi anak muda, terhindar dari kehamilan yang tidak diinginkan, kekerasan seksual, dan penyakit serius seperti HIV/AIDS. Di Indonesia, masalah kesehatan reproduksi ini diatur oleh Undang-Undang (UU) Kesehatan (UU No. 36/2009). Menurut UU ini, pemerintah dan masyarakat punya tanggung jawab berbagi informasi dan mendidik orang-orang tentang kesehatan reproduksi. Tujuannya supaya kita bisa mempunyai generasi yang sehat dan pertumbuhan populasi yang stabil. Tapi, adanya UU No.44 Tahun 2008 Tentang Pornografi (UU Ponografi) malah membuat penyebaran informasi tentang kesehatan reproduksi jadi terhambat. UU Pornografi menganggap "sketsa, ilustrasi, suara bunyi, kartun, percakapan, gerak tubuh atau bentuk pesan lainnya yang memuat kecabulan" sebagai materi pornografi. Artinya, materi edukasi kesehatan seksual bisa saja dianggap sebagai materi ponografi, jadi malah engga bisa disebarkan. Sementara itu, ada juga UU No. 1 Tahun 2023 tentang Rancangan Kitab Undang-Undang Hukum Pidana (RKUHP) yang membatasi siapa saja yang boleh memberi tau tentang alat kontrasepsi ke anak dan remaja. Di sini, peran masyarakat jadi terbatas karena hanya petugas berwenang yang boleh memberi pendidikan kesehatan reproduksi. Nah, pertanyaannya sekarang: Gimana caranya pemerintah bisa tetap memberi akses pendidikan kesehatan seksual dan reproduksi – yang emang hak asasi setiap orang Indonesia – kalau ada undang-undang yang malah menghambat penyebarannya?'
});

// ---- MERGE node constraint (unique nodes)
CREATE CONSTRAINT FOR (n:Parliament) REQUIRE (n.index) IS UNIQUE;
CREATE CONSTRAINT FOR (n:Principle) REQUIRE (n.index) IS UNIQUE ;
CREATE CONSTRAINT FOR (n:Political_Leaning) REQUIRE (n.index) IS UNIQUE; 
CREATE CONSTRAINT FOR (n:Economic_view) REQUIRE (n.index) IS UNIQUE;
CREATE CONSTRAINT FOR (n:RegionVote) REQUIRE (n.index) IS UNIQUE;
CREATE CONSTRAINT FOR (n:OfficePosition) REQUIRE (n.index) IS UNIQUE;
CREATE CONSTRAINT FOR (n:JenisKasus) REQUIRE (n.index) IS UNIQUE;
CREATE CONSTRAINT FOR (n:Law) REQUIRE (n.index) IS UNIQUE;
CREATE CONSTRAINT FOR (n:Issue) REQUIRE (n.index) IS UNIQUE;

// ---- Law - Issue Relationship
MATCH (a:Law {index:'UU_IKN'}), (b:Issue {index:'IbukotaNegara'})
    CREATE (a)-[:IS_RELATED_TO ]->(b);
MATCH (a:Law {index:'UU_EBT'}), (b:Issue {index:'TransisiEnergi'})
    CREATE (a)-[:IS_RELATED_TO ]->(b);
MATCH (a:Law {index:'UU_KPK'}), (b:Issue {index:'EradicatingCorruption'})
    CREATE (a)-[:IS_RELATED_TO ]->(b);
MATCH (a:Law {index:'UU_ITE'}), (b:Issue {index:'FreedomOfSpeech'})
    CREATE (a)-[:IS_RELATED_TO ]->(b);
MATCH (a:Law {index:'RUU_Adat'}), (b:Issue {index:'HakAdat'})
    CREATE (a)-[:IS_RELATED_TO ]->(b);
MATCH (a:Law {index:'KUHP'}), (b:Issue {index:'SexEducation'})
    CREATE (a)-[:IS_RELATED_TO ]->(b);
MATCH (a:Law {index:'KUHP'}), (b:Issue {index:'FreedomOfSpeech'})
    CREATE (a)-[:IS_RELATED_TO ]->(b);

// ---------- PARTY PAGE NODES --------------
// ---- Political Parties
MERGE (Golkar:Political_party {
            index:'Golkar',
            name:'Golongan Karya',
            alias:'Golkar',
            year_established:1964,
            unique_facts:'Warna kuning ikonik Golkar menjadi lambang kejayaan. Ada 17 bunga kapas, 8 cabang pohon   beringin, dan 45 butir padi, yang menceritakan tanggal kemerdekaan Indonesia. Latar belakang putih menggambarkan kemurnian agama sebagai prinsip pertama Pancasila.',
            description:'Berdiri tahun 1964, Partai Golongan Karya (Golkar) adalah salah satu partai politik tertua di Indonesia. Menurut ilmuwan politik Ulla Fionna dan Dirk Tomsa, Golkar masih sering diingat sebagai kendaraan politik kalangan elit zaman rezim Presiden Suharto. Sekarang, Golkar tetap menjadi partai yang kuat dengan pandangan politik tengah-kanan. Wakil Sekretaris Jenderal Golkar Puteri Komarudin menjelaskan bahwa Golkar menjadi ‘matang’ karena fokus ke pemberdayaan pemuda, ekonomi kreatif, dan pembaharuan sektor publik.'
    }
)

// ---- Person
MERGE (AirlanggaHartanto:Person {
        index:'AirlanggaHartanto',
        name:'Airlangga Hartanto',
        is_involved_in_corruption:False,
        description:'Airlangga adalah Menteri Koordinator Bidang Perekonomian saat ini yang memiliki pengalaman di usaha pertanian. Fokus kebijakannya ialah di digitalisasi industri, integrasi energi hijau, dan program bantuan usaha menengah kecil. Namun, belakangan ini Airlangga terancam kehilangan posisinya di Golkar karena ada dorongan internal untuk milih ketua umum yang lebih bisa menjamin kemenangan Golkar di Pemilu 2024.'
    }
)
MERGE (Luhut:Person {
        index:'Luhut',
        name:'Luhut Binsar Pandjaitan',
        is_involved_in_corruption:False,
        description:'Luhut Binsar Pandjaitan menjabat sebagai Menteri Koordinator Bidang Kemaritiman dan Investasi dan Ketua Dewan Penasihat Golkar. Sebelumnya, ia sempat ditunjuk sebagai Kepala Staf Kepresidenan Republik Indonesia (2014), Menteri Koordinator Bidang Politik, Hukum, dan Keamanan (2015), serta Plt. Menteri Energi dan Sumber Daya Mineral (2016). Banyak berpendapat bahwa Luhut memainkan peran penting selama pemerintahan Joko Widodo, termasuk dalam konteks penanganan pandemi. Menurut Tempo, Luhut didukung oleh kelompok yang bermaksud mengambil alih status Ketua Umum Partai Golkar dari Airlangga.'
    }
)
MERGE (Dito:Person {
        index:'Dito',
        name:'Ario Bimo Nandito Ariotedjo',
        is_involved_in_corruption:False,
        description:'Biasa dipanggil ‘Dito’, ia sekarang menjabat sebagai Menteri Pemuda dan Olahraga yang menjadi Menteri termuda di Kabinet Jokowi. Sebelum itu, Ia sempat menjadi Staff Khusus untuk Menteri Koordinator Bidang Perekonomian, Airlangga. Sembari jadi Kepala Lembaga Inovasi dan Kreativitas DPP Golkar, Dito ingin fokus membenarkan profesionalisme dan kurangnya kewirausahaan di sektor olahraga.'
    }
)
MERGE (AgusGumiwang:Person {
        index:'AgusGumiwang',
        name:'Agus Gumiwang Kartasasmita',
        is_involved_in_corruption:False,
        description:'Agus Gumiwang saat ini menjabat sebagai Menteri Perindustrian (sebelumnya Menteri Sosial 2018-2019, menggantikan Idrus Marham yang terjerat kasus korupsi). Agus mendorong target Indonesia sebagai negara industri tangguh pada tahun 2035, dengan bercirikan struktur industri nasional yang kuat, berdaya saing global, serta berbasis inovasi dan teknologi. Agus sempat dikritik oleh salah satu Anggota DPR Fraksi PKS terkait rencana subsidi kendaraan listrik yang harus tepat sasaran. Saat ini Ia menempati posisi Wakil Ketua Umum Koordinator Bidang Perekonomian Golkar.'
    }
)
MERGE (SetyaNovanto:Person {
        index:'SetyaNovanto',
        name:'Setya Novanto',
        is_involved_in_corruption:True,
        description:'Mantan Ketua Golkar ini sempat terjerat kasus negosiasi saham dengan Freeport Indonesia. Ia dihukum 15 tahun penjara untuk pelanggaran kode etik, karena obrolanya dengan Direktur Freeport Indonesia yang terekam. Sebelumnya, dampak legislatif Setya di DPR RI dinilai minim oleh Kompas, dan Ia dikiritik masyarakat karena menghabiskan Rp. 1,6 Triliun untuk proyek renovasi DPR.'
    }
) 
MERGE (IdrusMarham:Person {
        index:'IdrusMarham',
        name:'Idrus Marham',
        is_involved_in_corruption:True,
        description:'Idrus Marham merupakan Menteri Sosial kader Golkar yang dijatuhkan vonis selama tiga tahun karena terbukti menerima hadiah senilai Rp2,25 miliar dari pengusaha Johanes Budisutrisno Kotjo. Ia terbukti melakukan tindak pidana korupsi itu dalam kasus suap PLTU Riau 1.'
    }
)

MERGE (NurdinHalid:Person {
        index:'NurdinHalid',
        name:'Nurdin Halid',
        is_involved_in_corruption:True,
        description:''
    }
)
MERGE (DedeWidarso:Person {
        index:'DedeWidarso',
        name:'Dede Widarso',
        is_involved_in_corruption:True,
        description:''
    }
)
MERGE (RommyKrishnas:Person {
        index:'RommyKrishnas',
        name:'Rommy Krishnas',
        is_involved_in_corruption:True,
        description:''
    }
)

// ---- Corruption Case
MERGE (Korupsi_E_KTP:CorruptionCase {
    index:'Korupsi_E_KTP',
    name:'Korupsi E-KTP',
    description:'Korupsi proyek pengadaan Kartu Tanda Penduduk elektronik atau e-KTP',
    value:'~2.3 Trillion Rupiah'
})

MERGE (SUAP_PLTU_RIAU:CorruptionCase {
    index:'SUAP_PLTU_RIAU',
    name:'Suap PLTU Riau',
    description:'Kasus Suap proyek pembangunan Pembangkit Listrik Tenaga Uap (PLTU) di Riau',
    value:'2.25 Billion Rupiah'
})

MERGE (UNKNOWN_CASE:CorruptionCase {
    index:'UNKNOWN_CASE',
    name:'placeholder',
    description:'Placeholder for unspecified corrpution case'
});

// ---- Constraints 
CREATE CONSTRAINT FOR (n:Political_party) REQUIRE (n.index) IS UNIQUE;
CREATE CONSTRAINT FOR (n:Person) REQUIRE (n.index) IS UNIQUE;
CREATE CONSTRAINT FOR (n:CorruptionCase) REQUIRE (n.index) IS UNIQUE;

// ---------- EDGES --------------
// ---- 2019 election result
MATCH (a:Political_party {index:'Golkar'}), (b:RegionVote {index:'Gorontalo'})
    CREATE (a)-[:VOTE_WON_IN {percentage: 29.1, event:'2019 General Election'}]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:RegionVote {index:'Jambi'})
    CREATE (a)-[:VOTE_WON_IN {percentage: 21.4, event:'2019 General Election'}]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:RegionVote {index:'Sumsel'})
    CREATE (a)-[:VOTE_WON_IN {percentage: 20.2, event:'2019 General Election'}]->(b);


//---- Ideological Spectrum
MATCH (a:Political_party {index:'Golkar'}), (b:Principle {index:'Pancasila'})
    CREATE (a)-[:IS_BASED_ON_PRINCIPLE {Spectrum_Score: 7.83}]->(b);
// MATCH (a:Political_party {index:'Golkar'}), (b:Principle {index:'Islamic_religious'})
    CREATE (a)-[:IS_BASED_ON_PRINCIPLE {Spectrum_Score: 2.17}]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Principle {index:'Conservative'})
    CREATE (a)-[:IS_BASED_ON_PRINCIPLE {Spectrum_Score: 5.59}]->(b);
// MATCH (a:Political_party {index:'Golkar'}), (b:Principle {index:'Progressive'})
    CREATE (a)-[:IS_BASED_ON_PRINCIPLE {Spectrum_Score: 4.41}]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Principle {index:'Liberal_Economy'})
    CREATE (a)-[:IS_BASED_ON_PRINCIPLE {Spectrum_Score: 5.19}]->(b);
// MATCH (a:Political_party {index:'Golkar'}), (b:Principle {index:'Regulated_Economy'})
    CREATE (a)-[:IS_BASED_ON_PRINCIPLE {Spectrum_Score: 4.81}]->(b);

// Parliament Seat
MATCH (a:Political_party {index:'Golkar'}), (b:Parliament {index:'DPR'})
    CREATE (a)-[:HAVE_CURRENT_SEAT_IN {number_of_seat:85, percent_of_seat:14.8}]->(b);

// ---- Members
MATCH (a:Person {index:'AirlanggaHartanto'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Current Party Leader'}]->(b);
MATCH (a:Person {index:'Luhut'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Member'}]->(b);
MATCH (a:Person {index:'Dito'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Member'}]->(b);
MATCH (a:Person {index:'AgusGumiwang'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Member'}]->(b);
MATCH (a:Person {index:'SetyaNovanto'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Member'}]->(b);
MATCH (a:Person {index:'IdrusMarham'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Member'}]->(b);
MATCH (a:Person {index:'NurdinHalid'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Member'}]->(b);
MATCH (a:Person {index:'DedeWidarso'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Member'}]->(b);
MATCH (a:Person {index:'RommyKrishnas'}), (b:Political_party {index:'Golkar'})
    CREATE (a)-[:IS_MEMBER_OF {role:'Member'}]->(b);

// ---- Members (opposite direction)
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'AirlanggaHartanto'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'Luhut'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'Dito'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'AgusGumiwang'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'SetyaNovanto'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'IdrusMarham'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'NurdinHalid'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'DedeWidarso'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'RommyKrishnas'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER]->(b);




// ---- Nominated Corruptor
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'NurdinHalid'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER {nominated_for:'DPR RI', election_year:2024, region_vote:'Sulawesi Selatan II'}]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'DedeWidarso'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER {nominated_for:'DPRD Kabupaten', election_year:2024, region_vote:'Kabupaten Pandeglang 5'}]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Person {index:'RommyKrishnas'})
    CREATE (a)-[:PARTY_WHERE_PERSON_IS_MEMBER {nominated_for:'DPRD Kota', election_year:2024, region_vote:'Lubuk Linggau 3'}]->(b);

 



// ---- Corruption Case
MATCH (a:Person {index:'SetyaNovanto'}), (b:CorruptionCase {index:'Korupsi_E_KTP'})
    CREATE (a)-[:IS_A_CORRUPTION_CONVICT_DUE_TO {status:'convicted corruptor'}]->(b);
MATCH (a:Person {index:'IdrusMarham'}), (b:CorruptionCase {index:'SUAP_PLTU_RIAU'})
    CREATE (a)-[:IS_A_CORRUPTION_CONVICT_DUE_TO {status:'convicted corruptor'}]->(b);
MATCH (a:Person {index:'NurdinHalid'}), (b:CorruptionCase {index:'UNKNOWN_CASE'})
    CREATE (a)-[:IS_A_CORRUPTION_CONVICT_DUE_TO {status:'convicted corruptor'}]->(b);
MATCH (a:Person {index:'DedeWidarso'}), (b:CorruptionCase {index:'UNKNOWN_CASE'})
    CREATE (a)-[:IS_A_CORRUPTION_CONVICT_DUE_TO {status:'convicted corruptor'}]->(b);
MATCH (a:Person {index:'RommyKrishnas'}), (b:CorruptionCase {index:'UNKNOWN_CASE'})
    CREATE (a)-[:IS_A_CORRUPTION_CONVICT_DUE_TO {status:'convicted corruptor'}]->(b);

// ---- Corruption Case Type
MATCH (a:CorruptionCase {index:'Korupsi_E_KTP'}), (b:JenisKasus {index:'Korupsi'})
    CREATE (a)-[:IS_A]->(b);
MATCH (a:CorruptionCase {index:'SUAP_PLTU_RIAU'}), (b:JenisKasus {index:'Gratifikasi'})
    MERGE (a)-[:IS_A]->(b);

// ---- Stance
MATCH (a:Political_party {index:'Golkar'}), (b:Law {index:'UU_IKN'})
    CREATE (a)-[:IS_SUPPORTING {
        reason:'Semua pimpinan parpol yang hadir, mendukung rencana Jokowi dalam melanjutkan proyek IKN',
        source:'https://www.ikn.go.id/en/presiden-jokowi-tancap-gas-pindahkan-ibu-kota-ke-kaltim-pengusaha-kasih-dukungan-penuh'
    }]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Law {index:'UU_EBT'})
    CREATE (a)-[:IS_SUPPORTING {
        reason:'Anggota Komisi VII DPR RI Dyah Roro Esti mengharapkan RUU EB-ET mampu mempercepat proses transisi energi di Indonesia',
        source:'https://www.antaranews.com/berita/2971669/dyah-roro-esti-harapkan-ruu-ebet-percepat-transisi-energi-di-indonesia#mobile-src'
    }]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Law {index:'UU_KPK'})
    CREATE (a)-[:IS_SUPPORTING {
        reason:'Seluruh partai politik di DPR kompak menyepakati revisi UU KPK, tanpa memandang dukungan pada Pilpres 2019',
        source:'https://nasional.kompas.com/read/2019/09/18/08131291/fraksi-kompak-revisi-uu-kpk-tetapi-begini-faktanya'
    }]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Law {index:'UU_ITE'})
    CREATE (a)-[:IS_SUPPORTING {
        reason:'Politisi Golkar, Christina Aryani, menekankan kebutuhan revisi UU ITE untuk mengatasi keresahan interpretasi pasal-pasalnya',
        source:'https://www.dpr.go.id/berita/detail/id/43302/t/Sering+Timbulkan+Keresahan%2C+Komisi+I+Akan+Bahas+Revisi+UU+ITE'
    }]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Law {index:'KUHP'})
    CREATE (a)-[:IS_SUPPORTING {
        reason:'Seluruh fraksi di DPR setujui pengesahan RKUHP sebagai Undang-Undang pada Paripurna ke-11 tahun 2022-2023',
        source:'https://www.cnnindonesia.com/nasional/20221206115523-32-883441/semua-fraksi-setuju-rkuhp-disahkan-satu-kader-pks-walk-out'
    }]->(b);
MATCH (a:Political_party {index:'Golkar'}), (b:Law {index:'RUU_Adat'})
    CREATE (a)-[:IS_AGAINST {
        reason:'Fraksi Partai Golkar menolak RUU Masyarakat Hukum Adat untuk dilanjutkan karena setelah mereka kaji masih belum mendesak saat ini',
        source:'https://nasional.tempo.co/read/1423363/golkar-tolak-ruu-masyarakat-adat-dan-ruu-perlindungan-prt-di-prolegnas'
    }]->(b);


// --- Office Position
MATCH (a:Person {index:'AirlanggaHartanto'}), (b:OfficePosition {index:'MenteriKoordinatorEkonomi'})
    CREATE (a)-[:HOLDS_OFFICE_OF {current:True}]->(b);
MATCH (a:Person {index:'Luhut'}), (b:OfficePosition {index:'MenteriKoordinatorMaritim'})
    CREATE (a)-[:HOLDS_OFFICE_OF {current:True}]->(b);
MATCH (a:Person {index:'Dito'}), (b:OfficePosition {index:'MenteriPemudaDanOlahraga'})
    CREATE (a)-[:HOLDS_OFFICE_OF {current:True}]->(b);
MATCH (a:Person {index:'Luhut'}), (b:OfficePosition {index:'KepalaStafPresiden'})
    CREATE (a)-[:HOLDS_OFFICE_OF {current:False, start_year:2014, end_year:2014}]->(b);
MATCH (a:Person {index:'IdrusMarham'}), (b:OfficePosition {index:'MenteriSosial'})
    CREATE (a)-[:HOLDS_OFFICE_OF {current:False}]->(b);
MATCH (a:Person {index:'AgusGumiwang'}), (b:OfficePosition {index:'MenteriSosial'})
    CREATE (a)-[:HOLDS_OFFICE_OF {current:True}]->(b);
MATCH (a:Person {index:'AgusGumiwang'}), (b:OfficePosition {index:'MenteriPerindustrian'})
    CREATE (a)-[:HOLDS_OFFICE_OF {current:False, start_year:2018, end_year:2019}]->(b);
