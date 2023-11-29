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
	('Angel', 'M 2348 GHT', 'motor', 'pertamax', 3, '09:00', '2022-10-02')
	;