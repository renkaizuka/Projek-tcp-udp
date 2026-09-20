# Hybrid Socket: Sistem Distribusi Pesan & File (TCP + UDP)

Tugas Jaringan Komputer Lanjut (S2 Ilmu Komputer). Referensi: Kurose & Ross, *Computer Networking: A Top-Down Approach* 9th Ed., Section 2.6.

## Struktur

| File | Fungsi |
|------|--------|
| `protocol.py` | Protokol aplikasi: framing dengan header fixed-length 5 byte (1 byte TYPE + 4 byte LENGTH) |
| `TCPServer.py` | Server TCP multi-client (1 thread per client), chat broadcast & penyimpanan file |
| `TCPClient.py` | Client CLI: chat, unggah/unduh file, uji burst |
| `UDPServer.py` | Server heartbeat UDP (1 soket), dengan opsi simulasi packet loss & delay |
| `UDPClient.py` | Pinger: 10 ping, timeout 1 detik, RTT min/avg/max, EstimatedRTT, packet loss |
| `tcp_raw_demo.py` | Demonstrasi masalah message boundary TCP tanpa framing |

## Format Frame TCP

```
+--------+----------------------+-----------------+
| TYPE 1B| LENGTH 4B big-endian | PAYLOAD (LENGTH)|
+--------+----------------------+-----------------+
TYPE: 1=TEXT 2=FILE 3=CMD 4=INFO 5=ERROR
```

## Kebutuhan

Python 3.8+ saja, tanpa library tambahan.

## Cara Menjalankan

Buka beberapa terminal di folder repositori.

```bash
# Terminal 1 - server TCP
python TCPServer.py --port 12000

# Terminal 2 - server UDP (opsional: simulasi 30% loss)
python UDPServer.py --port 12001 --loss 0.3

# Terminal 3, 4, 5 - beberapa client TCP
python TCPClient.py --host 127.0.0.1 --port 12000

# Terminal lain - UDP pinger
python UDPClient.py --host 127.0.0.1 --port 12001
```

Perintah pada client TCP: `/nick <nama>`, `/users`, `/send <path>`, `/list`, `/get <nama>`, `/burst`, `/quit`, atau ketik teks biasa untuk chat.

## Skenario Pengujian

```bash
# Uji framing: 3 pesan tanpa delay diterima sebagai 3 pesan terpisah
python TCPClient.py --demo-burst

# Bandingkan dengan TCP tanpa framing (pesan tergabung)
python tcp_raw_demo.py server      # terminal A
python tcp_raw_demo.py client      # terminal B

# Balasan terlambat (uji pembuangan paket stale)
python UDPServer.py --loss 0.2 --delay 1.5

# Bind eksplisit port client (jalankan 2 kali bersamaan untuk melihat konflik)
python UDPClient.py --bind-port 5432 --count 20
```

Jika server berada di komputer lain, ganti `--host` dengan IP server dan izinkan port 12000/TCP serta 12001/UDP di firewall.
