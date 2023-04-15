use qqmusic;

CREATE TABLE `Songs` (
	`list_name` VARCHAR(255) NOT NULL,
	`rank` INT NOT NULL,
	`song_name` VARCHAR(255),
	`rank_ration` VARCHAR(255) NOT NULL,
	`singer` VARCHAR(255) NOT NULL,
	`song_time` VARCHAR(255) NOT NULL,
	`img_url` VARCHAR(255) NOT NULL,
	`info_list` VARCHAR(255) NOT NULL,
	`song_url` VARCHAR(255) NOT NULL,
	`comment_num` VARCHAR(255),
	PRIMARY KEY (`list_name`,`rank`)
);

CREATE TABLE `Comments` (
	`reviewer_name` VARCHAR(255) NOT NULL,
	`review_time` VARCHAR(255) NOT NULL,
	`song_name` VARCHAR(255) NOT NULL,
	`review_prov` VARCHAR(255) NOT NULL,
	`zan` VARCHAR(255),
	`review` VARCHAR(301) NOT NULL,
	PRIMARY KEY (`reviewer_name`,`review_time`)
);



