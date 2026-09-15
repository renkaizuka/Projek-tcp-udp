## Panduan Sniffing dengan Wireshark

Karena kamu barusan menjalankan `webserver.py` (TCP port 6789) dan `UDPPingerClient.py`/`UDPPingerServer.py` (UDP port 12000) via `127.0.0.1`, ada satu hal penting yang perlu diperhatikan dulu: **trafik ke localhost tidak lewat network adapter biasa**, jadi Wireshark standar tidak akan menangkapnya kecuali kamu aktifkan adapter loopback. Berikut langkah lengkapnya untuk Windows.

### 1. Pastikan Wireshark + Npcap terpasang
Kalau belum ada, download dari wireshark.org dan install (installer-nya otomatis menyertakan Npcap, driver capture-nya). Saat instalasi Npcap, centang opsi **"Support raw 802.11 traffic..."** tidak wajib, tapi pastikan **"Install Npcap in WinPcap API-compatible Mode"** dicentang (default).

### 2. Pilih interface yang tepat
Buka Wireshark, lihat daftar interface:
- Kalau server & client kamu jalan di komputer yang **sama** lewat `127.0.0.1` (seperti testing yang barusan) → pilih interface **"Adapter for loopback traffic capture"** (kadang muncul sebagai `Npcap Loopback Adapter`). Tanpa ini, capture-mu akan kosong walaupun program jalan normal.
- Kalau server & client dijalankan di **dua host berbeda** di jaringan yang sama (sesuai instruksi tugas Web Server yang minta test dari host lain) → pilih interface Wi-Fi/Ethernet aktif kamu, trafiknya akan otomatis muncul karena benar-benar lewat NIC.

Tips: kalau ragu mau capture localhost vs LAN, cara paling gampang untuk lab ini justru **jalankan server pakai IP LAN asli** (bukan `127.0.0.1`) dan akses dari device lain — jadi kamu langsung capture di interface normal tanpa perlu ribet soal loopback adapter.

### 3. Pasang capture filter sebelum mulai (opsional tapi disarankan)
Biar tidak kebanjiran trafik lain, isi kolom filter di layar awal sebelum klik start:
- Untuk Web Server: `port 6789` atau `tcp port 6789`
- Untuk UDP Pinger: `port 12000` atau `udp port 12000`

### 4. Mulai capture, lalu jalankan program
- Klik ikon capture (start) di Wireshark.
- Untuk Web Server: jalankan `webserver.py`, lalu akses `http://<ip-server>:6789/HelloWorld.html` dari browser (atau `curl`).
- Untuk UDP Pinger: jalankan `UDPPingerServer.py`, lalu `UDPPingerClient.py`.
- Biarkan capture berjalan sampai selesai request/10 ping, baru klik stop (kotak merah).

### 5. Analisa hasil capture
**Web Server (TCP/HTTP):**
- Kalau belum otomatis terdeteksi sebagai HTTP, gunakan display filter `tcp.port == 6789` atau `http`.
- Klik kanan salah satu paket → **Follow → TCP Stream** untuk lihat full percakapan: 3-way handshake (SYN, SYN-ACK, ACK), request `GET /HelloWorld.html HTTP/1.1`, lalu response `HTTP/1.1 200 OK` beserta isi HTML-nya. Ini bagus dijadikan bukti screenshot untuk laporan tugas.
- Coba juga request file yang tidak ada, filter ulang, lihat response `404 Not Found`.

**UDP Pinger:**
- Display filter `udp.port == 12000`.
- Klik satu paket dari client → lihat di panel bawah bagian **Data** untuk payload `Ping <seq> <time>`.
- Cari paket balasan dari server (isinya huruf kapital semua, misal `PING 2 ...`) — bandingkan timestamp-nya untuk verifikasi RTT.
- Kalau ada ping yang timeout (hilang di client), kamu akan lihat di capture hanya ada paket request dari client tanpa paket balasan dari server — ini bukti nyata dari simulasi packet loss 30-40% di kode server.

### 6. Simpan hasilnya
- **File → Save As** → simpan sebagai `.pcapng` kalau dosen minta file capture asli (biar konsisten dengan file-file di folder `wireshark` kamu yang lain).
- Atau langsung screenshot jendela Wireshark yang menunjukkan paket-paket relevan untuk dilampirkan ke laporan.
