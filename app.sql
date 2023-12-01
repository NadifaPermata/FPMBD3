drop table if exists selling;
create table selling (
	id serial,
	nama_petugas text,
	plat_nomor text,
	jenis_kendaraan text,
	bbm text,
	banyak_pembelian text,
	waktu time,
	tanggal date
);

insert into selling (nama_petugas, plat_nomor, jenis_kendaraan, bbm, banyak_pembelian, waktu, tanggal) 
values
	('Nuryanto', 'L 0919 CGF', 'mobil','pertamax turbo', 5, '08:00', '2023-10-01'),
	('Angel', 'M 2348 GHT', 'motor', 'pertamax', 3, '09:00', '2022-10-02'),
	('Angel', 'N 1087 AE', 'motor', 'pertamax', 2, '20:00', '2021-12-12'),
	('Nuryanto', 'AE 2047 E', 'motor', 'pertamax', 3, '20:00', '2022-02-12')
	('Angel', 'AG 0887 A', 'truk', 'solar', 10, '18:00', '2021-12-24')
	;