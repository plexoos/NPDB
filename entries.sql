truncate "GlobalTag", "GlobalTagStatus", "GlobalTagType", "PayloadIOV", "PayloadList", "PayloadListIdSequence", "PayloadType" restart identity cascade;
insert into "GlobalTagStatus" values (1, 'test', null, current_timestamp);
insert into "GlobalTagType"   values (1, 'test', null, current_timestamp);

insert into "PayloadType" values (1, 'Domain_1', null, current_timestamp);
insert into "PayloadType" values (2, 'Domain_2', null, current_timestamp);

insert into "GlobalTag" values (1, 'Tag_1', '', current_timestamp, current_timestamp, 1, 1);
insert into "PayloadList" values (1, 'Domain_1_Tag_1', null, current_timestamp, current_timestamp, 1, 1);
insert into "PayloadIOV" values (1, 'Payload_1_Commit_1_Domain_1', 0, 1, 0, 0, null, current_timestamp, current_timestamp, 1);
insert into "PayloadIOV" values (2, 'Payload_2_Commit_1_Domain_1', 0, 2, 0, 0, null, current_timestamp, current_timestamp, 1);
insert into "PayloadList" values (2, 'Domain_2_Tag_1', null, current_timestamp, current_timestamp, 1, 2);
insert into "PayloadIOV" values (3, 'Payload_1_Commit_1_Domain_2', 0, 1, 0, 0, null, current_timestamp, current_timestamp, 2);
insert into "PayloadIOV" values (4, 'Payload_2_Commit_1_Domain_2', 0, 2, 0, 0, null, current_timestamp, current_timestamp, 2);

insert into "GlobalTag" values (2, 'Tag_2', '', current_timestamp, current_timestamp, 1, 1);
insert into "PayloadList" values (3, 'Domain_1_Tag_2', null, current_timestamp, current_timestamp, 2, 1);
insert into "PayloadIOV" values (5, 'Payload_1_Commit_2_Domain_1', 0, 1, 0, 0, null, current_timestamp, current_timestamp, 1);
insert into "PayloadIOV" values (6, 'Payload_2_Commit_2_Domain_1', 0, 2, 0, 0, null, current_timestamp, current_timestamp, 1);
insert into "PayloadList" values (4, 'Domain_2_Tag_2', null, current_timestamp, current_timestamp, 2, 2);
insert into "PayloadIOV" values (7, 'Payload_1_Commit_2_Domain_2', 0, 1, 0, 0, null, current_timestamp, current_timestamp, 2);
insert into "PayloadIOV" values (8, 'Payload_2_Commit_2_Domain_2', 0, 2, 0, 0, null, current_timestamp, current_timestamp, 2);

