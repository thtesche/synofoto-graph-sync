# Synofoto Database Schema

## Table: `acl_permission`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| fullpath | text | NO |  |
| permission | text | NO |  |
| type | smallint | NO |  |
| id_type | integer | NO |  |


## Table: `activity`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('activity_id_seq'::regclass) |
| id_user | integer | NO |  |
| id_album | integer | NO |  |
| type | smallint | NO |  |
| create_time | bigint | NO |  |


## Table: `address`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('address_id_seq'::regclass) |
| lang | smallint | NO |  |
| admin | smallint | NO |  |
| level | integer | NO |  |
| value | text | NO |  |
| id_unit | integer | YES |  |
| id_user | integer | NO |  |


## Table: `administrative`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('administrative_id_seq'::regclass) |
| value | text | NO |  |


## Table: `album`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('album_id_seq'::regclass) |
| id_user | integer | NO |  |
| name | text | NO |  |
| type | smallint | NO |  |
| shared | boolean | NO | false |
| create_time | bigint | NO |  |
| cover | integer | NO | 0 |
| sort_by | smallint | NO | 0 |
| sort_direction | smallint | NO | 0 |
| normalized_name | text | NO | ''::text |
| version | bigint | NO |  |
| passphrase_share | text | YES |  |
| item_count | integer | YES |  |
| start_time | bigint | YES |  |
| end_time | bigint | YES |  |
| name_for_sort | text | NO | ''::text |


## Table: `album_with_share_info_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | YES |  |
| id_user | integer | YES |  |
| name | text | YES |  |
| type | smallint | YES |  |
| create_time | bigint | YES |  |
| start_time | bigint | YES |  |
| privacy_type | smallint | YES |  |
| enable | boolean | YES |  |
| passphrase_share | text | YES |  |
| status | smallint | YES |  |
| name_for_sort | text | YES |  |


## Table: `aperture`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('aperture_id_seq'::regclass) |
| name | text | NO |  |
| normalized_name | text | NO |  |


## Table: `async_db_migration_task`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('async_db_migration_task_id_seq'::regclass) |
| id_user | integer | NO |  |
| target_version | integer | NO |  |
| payload | json | YES |  |


## Table: `background_task`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('background_task_id_seq'::regclass) |
| operation | smallint | NO |  |
| status | smallint | NO |  |
| created_time | bigint | NO |  |
| modified_time | bigint | NO |  |
| total | bigint | NO |  |
| completion | bigint | NO |  |
| error | bigint | NO |  |
| id_user | integer | NO |  |
| extra_info | text | YES |  |
| payload | json | YES |  |
| skip | bigint | NO | 0 |
| overwrite | bigint | NO | 0 |


## Table: `burst_additional`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| grouping_key | text | NO |  |
| sequence | bigint | NO |  |
| id_unit | integer | YES |  |
| id_user | integer | NO |  |


## Table: `camera`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('camera_id_seq'::regclass) |
| name | text | NO |  |
| normalized_name | text | NO |  |


## Table: `check_album_task`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('check_album_task_id_seq'::regclass) |
| id_user | integer | NO | 0 |
| id_group | integer | NO | 0 |
| id_folder | integer | NO | 0 |
| status | smallint | NO | 0 |


## Table: `cluster`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('cluster_id_seq'::regclass) |
| id_person | integer | YES |  |
| id_user | integer | NO |  |
| is_manual | boolean | NO | false |


## Table: `concept`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('concept_id_seq'::regclass) |
| stem | text | NO |  |
| hidden | boolean | NO | false |
| display_threshold | smallint | NO |  |
| confidence_threshold | numeric | YES |  |
| parent | ARRAY | NO |  |
| sort_index | integer | NO | '-1'::integer |


## Table: `concept_album_additional`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_concept | integer | NO |  |
| id_user | integer | NO |  |
| item_count | bigint | NO |  |
| custom_cover_id_unit | integer | YES |  |
| visibility_status | smallint | NO | 0 |


## Table: `concept_rawdata`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| result | json | NO |  |
| need_migrate | boolean | NO | false |
| version | integer | NO |  |
| id_user | integer | NO |  |


## Table: `concept_synonym`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| lang | smallint | NO |  |
| id_concept | integer | NO |  |
| synonym | text | NO |  |
| priority | smallint | NO |  |
| normalized_synonym | text | NO | ''::text |


## Table: `concept_threshold`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_concept | integer | NO |  |
| version | smallint | NO |  |
| confidence_threshold | numeric | NO |  |


## Table: `concept_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| id_unit | integer | YES |  |
| id_concept | ARRAY | YES |  |
| takentime | bigint | YES |  |


## Table: `condition_album`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('album_id_seq'::regclass) |
| id_user | integer | NO |  |
| name | text | NO |  |
| type | smallint | NO |  |
| shared | boolean | NO | false |
| create_time | bigint | NO |  |
| cover | integer | NO | 0 |
| sort_by | smallint | NO | 0 |
| sort_direction | smallint | NO | 0 |
| normalized_name | text | NO | ''::text |
| version | bigint | NO |  |
| passphrase_share | text | YES |  |
| item_count | integer | YES |  |
| condition | json | YES |  |
| start_time | bigint | YES |  |
| end_time | bigint | YES |  |
| name_for_sort | text | NO | ''::text |
| need_update_item | boolean | NO | false |
| item_update_version | bigint | NO | 0 |


## Table: `condition_album_item_2`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | NO |  |


## Table: `condition_album_item_5`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | NO |  |


## Table: `config`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| key | text | NO |  |
| value | text | NO |  |


## Table: `convert_thumbnail_allocation`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| session_id | text | NO |  |
| sent_to_client | boolean | NO |  |
| id | integer | NO |  |
| id_user | integer | NO |  |
| filename | text | NO |  |
| unit_type | smallint | NO |  |
| item_type | smallint | NO |  |
| status | smallint | NO |  |
| lower_extension | text | NO |  |
| thumbnail_type | ARRAY | NO |  |
| created_at | timestamp without time zone | NO | now() |


## Table: `delete_album`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_normal_album | integer | NO |  |
| id_user | integer | NO |  |
| version | bigint | NO |  |


## Table: `delete_condition_album`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_condition_album | integer | NO |  |
| id_user | integer | NO |  |
| version | bigint | NO |  |


## Table: `delete_item`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | NO |  |
| id_user | integer | NO |  |
| version | bigint | NO |  |
| reason | integer | NO | 0 |


## Table: `dsm_group`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| gid | bigint | NO |  |
| name | text | NO |  |


## Table: `dsm_user`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| uid | bigint | NO |  |
| name | text | NO |  |


## Table: `exposure_time`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('exposure_time_id_seq'::regclass) |
| name | text | NO |  |
| normalized_name | text | NO |  |


## Table: `face`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('face_id_seq'::regclass) |
| id_user | integer | NO |  |
| bounding_box | json | NO |  |
| landmark | json | YES |  |
| feature | bytea | YES |  |
| picture | oid | YES |  |
| score | integer | NO |  |
| id_unit | integer | YES |  |
| ref_id_unit | integer | NO |  |
| id_person_group | integer | YES |  |
| id_person | integer | YES |  |
| is_manual | boolean | NO | false |


## Table: `favorite_timeline`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | NO |  |
| id_user | integer | NO |  |
| item_type | integer | NO |  |
| unit_type | integer | NO |  |
| id_unit | integer | NO |  |
| id_favorite_user | ARRAY | NO |  |
| takentime | bigint | NO | 0 |


## Table: `file_operation_error`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_task | integer | NO |  |
| target_type | smallint | NO |  |
| target_id | integer | NO |  |
| reason | smallint | NO |  |


## Table: `file_operation_task`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_task | integer | NO |  |
| target_folder_id | integer | NO |  |
| policy | smallint | NO |  |
| id_user | integer | NO |  |
| id_item | ARRAY | NO |  |
| id_folder | ARRAY | NO |  |
| target_folder_id_user | integer | NO |  |


## Table: `filter`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_filter | integer | NO |  |
| filter_type | text | NO |  |
| id_user | integer | NO |  |


## Table: `focal_length`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('focal_length_id_seq'::regclass) |
| name | text | NO |  |
| normalized_name | text | NO |  |


## Table: `folder`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('folder_id_seq'::regclass) |
| id_user | integer | NO |  |
| name | text | NO |  |
| parent | integer | NO |  |
| name_for_sort | text | NO | ''::text |
| permission | text | YES |  |
| mtime | bigint | NO | 0 |
| passphrase_share | text | YES |  |
| shared | boolean | NO |  |
| sort_by | smallint | NO | 0 |
| sort_direction | smallint | NO | 0 |
| permission_parent | integer | NO | 0 |
| name_for_search | text | NO | ''::text |
| normalized_name | text | NO | ''::text |


## Table: `folder_operation_error`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_task | integer | NO |  |
| target_id | integer | NO |  |
| reason | smallint | NO |  |


## Table: `folder_operation_task`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_folder | integer | NO |  |
| id_task | integer | NO |  |


## Table: `folder_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| id_unit | integer | YES |  |
| id_folder | integer | YES |  |
| takentime | bigint | YES |  |
| filesize | bigint | YES |  |
| normalized_filename | text | YES |  |
| name_for_sort | text | YES |  |


## Table: `general_tag`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('general_tag_id_seq'::regclass) |
| id_user | integer | NO |  |
| name | text | NO |  |
| count | integer | NO | 0 |
| normalized_name | text | NO | ''::text |
| name_for_sort | text | NO | ''::text |


## Table: `general_tag_album_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_general_tag | integer | YES |  |
| name | text | YES |  |
| normalized_name | text | YES |  |
| item_count | bigint | YES |  |
| id_user | integer | YES |  |


## Table: `general_tag_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| id_unit | integer | YES |  |
| id_general_tag | ARRAY | YES |  |
| takentime | bigint | YES |  |


## Table: `geocoding`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('geocoding_id_seq'::regclass) |
| id_user | integer | NO |  |
| grouping_key | text | NO |  |
| level_1 | integer | YES |  |
| level_2 | integer | YES |  |
| level_3 | integer | YES |  |
| level_4 | integer | YES |  |
| level_5 | integer | YES |  |
| level_6 | integer | YES |  |
| admin_1 | smallint | YES |  |
| admin_2 | smallint | YES |  |
| admin_3 | smallint | YES |  |
| admin_4 | smallint | YES |  |
| admin_5 | smallint | YES |  |
| admin_6 | smallint | YES |  |


## Table: `geocoding_album_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_geocoding | integer | YES |  |
| id_user | integer | YES |  |
| item_count | bigint | YES |  |
| album_count | bigint | YES |  |
| level_1 | integer | YES |  |


## Table: `geocoding_info`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('geocoding_info_id_seq'::regclass) |
| id_user | integer | NO |  |
| lang | smallint | NO |  |
| first_level | text | NO |  |
| second_level | text | NO |  |
| country | text | NO |  |
| id_geocoding | integer | YES |  |


## Table: `geocoding_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| takentime | bigint | YES |  |
| id_unit | integer | YES |  |
| id_geocoding | integer | YES |  |


## Table: `group_info`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('group_info_id_seq'::regclass) |
| gid | bigint | YES |  |
| name | text | NO |  |
| enable | boolean | NO | false |


## Table: `index_queue`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('index_queue_id_seq'::regclass) |
| id_user | integer | NO |  |
| id_unit | integer | NO |  |
| type | smallint | NO | 0 |
| status | smallint | NO | 0 |
| task | bytea | NO |  |


## Table: `iso`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('iso_id_seq'::regclass) |
| name | text | NO |  |
| normalized_name | text | NO |  |


## Table: `item`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('item_id_seq'::regclass) |
| id_user | integer | NO |  |
| type | smallint | NO |  |
| id_similar_group | integer | YES |  |
| is_similar_top_pick | boolean | YES |  |


## Table: `lens`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('lens_id_seq'::regclass) |
| name | text | NO |  |
| normalized_name | text | NO |  |


## Table: `level_1_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| takentime | bigint | YES |  |
| id_unit | integer | YES |  |
| level | integer | YES |  |
| admin | smallint | YES |  |


## Table: `level_2_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| takentime | bigint | YES |  |
| id_unit | integer | YES |  |
| level | integer | YES |  |
| admin | smallint | YES |  |


## Table: `level_3_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| takentime | bigint | YES |  |
| id_unit | integer | YES |  |
| level | integer | YES |  |
| admin | smallint | YES |  |


## Table: `level_4_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| takentime | bigint | YES |  |
| id_unit | integer | YES |  |
| level | integer | YES |  |
| admin | smallint | YES |  |


## Table: `level_5_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| takentime | bigint | YES |  |
| id_unit | integer | YES |  |
| level | integer | YES |  |
| admin | smallint | YES |  |


## Table: `level_6_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| takentime | bigint | YES |  |
| id_unit | integer | YES |  |
| level | integer | YES |  |
| admin | smallint | YES |  |


## Table: `live`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| type | smallint | YES |  |
| filename | text | YES |  |
| filesize | bigint | YES |  |
| createtime | bigint | YES |  |
| takentime | bigint | YES |  |
| mtime | bigint | YES |  |
| duplicate_hash | text | YES |  |
| cache_key | text | YES |  |
| resolution | json | YES |  |
| index_stage | smallint | YES |  |
| version | bigint | YES |  |
| id_item | integer | YES |  |
| id_folder | integer | YES |  |
| id_geocoding | integer | YES |  |
| is_major | boolean | YES |  |
| grouping_key | text | YES |  |
| name_no_ext | text | YES |  |


## Table: `live_additional`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| grouping_key | text | NO |  |
| id_unit | integer | YES |  |


## Table: `many_item_has_many_normal_album`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| sequence | double precision | NO | 0 |
| item_provider_id_user | integer | YES |  |
| id_item | integer | NO |  |
| id_normal_album | integer | NO |  |
| album_id_user | integer | NO |  |


## Table: `many_unit_has_many_administrative`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_administrative | integer | NO |  |
| id_user | integer | YES |  |


## Table: `many_unit_has_many_concept`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_concept | integer | NO |  |
| id_user | integer | NO |  |
| confidence | numeric | NO |  |


## Table: `many_unit_has_many_favorite_user`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_user | integer | NO |  |
| id_favorite_user | integer | NO |  |


## Table: `many_unit_has_many_general_tag`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_general_tag | integer | NO |  |


## Table: `many_unit_has_many_person`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_person | integer | NO |  |
| id_user | integer | YES |  |


## Table: `metadata`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | YES |  |
| description | text | NO |  |
| orientation | smallint | NO | 1 |
| focal_length | text | NO |  |
| iso | text | NO |  |
| exposure_time | text | NO |  |
| aperture | text | NO |  |
| lens | text | NO |  |
| camera | text | NO |  |
| latitude | double precision | YES |  |
| longitude | double precision | YES |  |
| flash | smallint | YES |  |
| orientation_original | smallint | NO | 1 |
| rating | smallint | NO | 0 |
| normalized_description | text | NO | ''::text |


## Table: `mobile_config`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| uuid | text | NO |  |
| config | text | NO |  |


## Table: `motion_photo_additional`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| duration | bigint | NO |  |
| video_info | json | NO |  |
| audio_info | json | NO |  |
| id_unit | integer | YES |  |


## Table: `need_convert_thumbnail_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | YES |  |
| id_user | integer | YES |  |
| filename | text | YES |  |
| unit_type | smallint | YES |  |
| item_type | smallint | YES |  |
| codec | text | YES |  |
| status | smallint | YES |  |
| lower_extension | text | YES |  |
| thumbnail_type | ARRAY | YES |  |


## Table: `normal_album`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('album_id_seq'::regclass) |
| id_user | integer | NO |  |
| name | text | NO |  |
| type | smallint | NO |  |
| shared | boolean | NO | false |
| create_time | bigint | NO |  |
| cover | integer | NO | 0 |
| sort_by | smallint | NO | 0 |
| sort_direction | smallint | NO | 0 |
| normalized_name | text | NO | ''::text |
| version | bigint | NO |  |
| passphrase_share | text | YES |  |
| item_count | integer | YES |  |
| cant_migrate_condition | json | YES |  |
| condition | json | YES |  |
| status | smallint | NO | 0 |
| start_time | bigint | YES |  |
| end_time | bigint | YES |  |
| name_for_sort | text | NO | ''::text |


## Table: `normal_album_photowall_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_normal_album | integer | YES |  |
| id_item | integer | YES |  |
| item_provider_id_user | integer | YES |  |
| id_unit | integer | YES |  |
| takentime | bigint | YES |  |
| filesize | bigint | YES |  |
| normalized_filename | text | YES |  |
| sequence | double precision | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| name_for_sort | text | YES |  |


## Table: `notification`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_user | integer | NO |  |
| event | text | NO |  |
| target_id | integer | NO |  |


## Table: `one_filter_has_many_unit`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_aperture | integer | YES |  |
| id_camera | integer | YES |  |
| id_exposure_time | integer | YES |  |
| id_flash | integer | YES |  |
| id_focal_length | integer | YES |  |
| id_folder | integer | YES |  |
| id_iso | integer | YES |  |
| id_item_type | integer | YES |  |
| id_lens | integer | YES |  |
| id_takentime | integer | YES |  |
| id_user | integer | YES |  |
| id_rating | smallint | NO | 0 |
| is_major | boolean | NO | true |


## Table: `person`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('person_id_seq'::regclass) |
| id_user | integer | NO |  |
| name | text | NO |  |
| hidden | boolean | NO | false |
| custom_cover | boolean | NO | false |
| cover | integer | YES |  |
| normalized_name | text | NO | ''::text |
| created_time | bigint | NO | 0 |


## Table: `person_album_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_person | integer | YES |  |
| id_user | integer | YES |  |
| name | text | YES |  |
| hidden | boolean | YES |  |
| cover | integer | YES |  |
| item_count | bigint | YES |  |
| normalized_name | text | YES |  |


## Table: `person_face_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | YES |  |
| id_user | integer | YES |  |
| id_person | integer | YES |  |
| id_unit | integer | YES |  |
| score | integer | YES |  |
| is_major | boolean | YES |  |
| id_item | integer | YES |  |


## Table: `person_group`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('person_group_id_seq'::regclass) |
| weight | integer | YES |  |
| feature | bytea | YES |  |
| id_user | integer | NO |  |
| id_cluster | integer | YES |  |
| is_manual | boolean | NO | false |


## Table: `person_item_count`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_person | integer | NO |  |
| id_user | integer | NO |  |
| item_count | bigint | YES |  |


## Table: `person_migration_mapping`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_user | integer | NO |  |
| id_person_source | integer | NO |  |
| id_person | integer | NO |  |
| named_by_migration | boolean | NO |  |


## Table: `person_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| id_unit | integer | YES |  |
| id_person | ARRAY | YES |  |
| takentime | bigint | YES |  |


## Table: `photo_request`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| passphrase_share | text | NO |  |
| id_user | integer | NO |  |
| modified_time | bigint | NO |  |
| filesize_limit | bigint | NO | 0 |
| subject | text | NO |  |
| description | text | NO | ''::text |
| id_album | integer | YES |  |
| album_passphrase_share | text | YES |  |
| folder_id_user | integer | NO |  |
| folder_home_path | text | NO |  |


## Table: `recently_added_timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| createtime | bigint | YES |  |
| id_unit | integer | YES |  |


## Table: `regenerating_thumbnail_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | YES |  |
| id_user | integer | YES |  |
| filename | text | YES |  |
| unit_type | smallint | YES |  |
| status | smallint | YES |  |
| thumbnail_type | smallint | YES |  |


## Table: `search_timeline`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | NO |  |
| id_user | integer | NO |  |
| item_type | smallint | NO | 0 |
| unit_type | smallint | NO |  |
| takentime | bigint | NO | 0 |
| id_unit | integer | NO |  |


## Table: `share`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| passphrase | text | NO |  |
| privacy_type | smallint | NO | 0 |
| modified_time | bigint | NO | 0 |
| id_user | integer | NO |  |
| expired_time | bigint | NO |  |
| hashed_password | text | NO |  |
| enable | boolean | NO |  |
| type | smallint | NO |  |


## Table: `share_album_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | YES |  |
| id_user | integer | YES |  |
| name | text | YES |  |
| type | smallint | YES |  |
| shared | boolean | YES |  |
| create_time | bigint | YES |  |
| cover | integer | YES |  |
| sort_by | smallint | YES |  |
| sort_direction | smallint | YES |  |
| passphrase_share | text | YES |  |
| version | bigint | YES |  |
| item_count | integer | YES |  |
| modified_time | bigint | YES |  |
| normalized_name | text | YES |  |
| start_time | bigint | YES |  |
| end_time | bigint | YES |  |
| name_for_sort | text | YES |  |


## Table: `share_permission`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('share_permission_id_seq'::regclass) |
| id_user | integer | NO |  |
| permission | smallint | NO |  |
| target_type | smallint | NO |  |
| target_id | integer | NO |  |
| passphrase_share | text | NO |  |


## Table: `share_with_member_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | YES |  |
| permission | smallint | YES |  |
| target_type | smallint | YES |  |
| target_id | integer | YES |  |
| id_user | integer | YES |  |
| passphrase | text | YES |  |
| type | smallint | YES |  |
| expired_time | bigint | YES |  |
| modified_time | bigint | YES |  |


## Table: `similar_group`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('similar_group_id_seq'::regclass) |
| id_user | integer | NO |  |
| top_pick | integer | YES |  |
| item_count | integer | NO |  |
| update_at | bigint | NO |  |
| custom_top_pick | boolean | NO | false |
| version | bigint | NO |  |


## Table: `similar_hash`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_user | integer | NO |  |
| pdq_hash | ARRAY | YES |  |
| takentime | bigint | YES |  |
| need_action | boolean | NO | true |
| skip | boolean | NO | false |
| is_major | boolean | NO |  |
| id_item | integer | NO |  |
| type | smallint | NO | 0 |


## Table: `similar_timeline`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| id_item | integer | NO |  |
| id_user | integer | NO |  |
| takentime | bigint | YES |  |
| id_similar_group | integer | YES |  |
| similar_group_item_count | integer | YES |  |


## Table: `split_filename`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | NO |  |
| name | text | NO |  |
| lower_extension | text | NO |  |


## Table: `takentime`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('takentime_id_seq'::regclass) |
| takentime_day | text | NO |  |
| takentime_month | text | NO |  |
| takentime | bigint | NO | 0 |


## Table: `team_library_folder_has_many_sorting`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_user | integer | NO |  |
| id_folder | integer | NO |  |
| sort_by | smallint | NO | 0 |
| sort_direction | smallint | NO | 0 |


## Table: `team_library_group_permission`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_group | integer | NO |  |
| permission | smallint | NO | 0 |
| auto_backup | boolean | NO | false |


## Table: `team_library_user_permission`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_user | integer | NO |  |
| permission | smallint | NO | 0 |
| auto_backup | boolean | NO | false |


## Table: `thumb_preview`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| picture | oid | NO |  |
| id_unit | integer | NO |  |


## Table: `thumbnail`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| type | smallint | NO |  |
| status | smallint | NO |  |
| id_unit | integer | YES |  |


## Table: `thumbnail_version`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_user | integer | NO |  |
| id_unit | integer | NO |  |
| version | bigint | NO |  |
| sm_size_hash | text | NO | ''::text |


## Table: `timeline_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_item | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| takentime | bigint | YES |  |
| id_unit | integer | YES |  |


## Table: `udc_event`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_user | integer | NO |  |
| timestamp | bigint | NO |  |
| type | text | NO |  |
| payload | text | YES |  |


## Table: `udc_statistic`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_user | integer | NO |  |
| key | text | NO |  |
| value | text | NO |  |


## Table: `unit`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('unit_id_seq'::regclass) |
| id_user | integer | NO |  |
| type | smallint | NO | 0 |
| item_type | smallint | NO | 0 |
| filename | text | NO |  |
| filesize | bigint | NO | 0 |
| createtime | bigint | NO | 0 |
| mtime | bigint | NO | 0 |
| takentime | bigint | NO | 0 |
| duplicate_hash | text | NO |  |
| cache_key | text | NO |  |
| resolution | json | NO |  |
| index_stage | smallint | NO |  |
| version | bigint | NO |  |
| id_geocoding | integer | YES |  |
| id_item | integer | NO |  |
| mobile_cache_mtime | bigint | NO | 0 |
| reindex_flag | smallint | NO | 0 |
| normalized_filename | text | NO | ''::text |
| is_major | boolean | NO |  |
| id_folder | integer | NO |  |
| name_for_sort | text | NO | ''::text |
| index_version | integer | NO | 1 |


## Table: `unit_file_extension_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_unit | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| unit_type | smallint | YES |  |
| extension | text | YES |  |


## Table: `unit_to_general_tag_view`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_general_tag | integer | YES |  |
| name | text | YES |  |
| name_for_sort | text | YES |  |
| id_unit | integer | YES |  |
| id_user | integer | YES |  |


## Table: `user_event_history_0`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO |  |
| id_user | integer | NO |  |
| target_type | smallint | NO |  |
| target_id | ARRAY | NO |  |
| target_id_user | integer | NO |  |
| trigger_id_user | integer | YES |  |
| event_type | text | NO |  |
| event_detail | json | YES |  |


## Table: `user_event_history_1`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO |  |
| id_user | integer | NO |  |
| target_type | smallint | NO |  |
| target_id | ARRAY | NO |  |
| target_id_user | integer | NO |  |
| trigger_id_user | integer | YES |  |
| event_type | text | NO |  |
| event_detail | json | YES |  |


## Table: `user_event_history_2`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO |  |
| id_user | integer | NO |  |
| target_type | smallint | NO |  |
| target_id | ARRAY | NO |  |
| target_id_user | integer | NO |  |
| trigger_id_user | integer | YES |  |
| event_type | text | NO |  |
| event_detail | json | YES |  |


## Table: `user_event_history_3`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO |  |
| id_user | integer | NO |  |
| target_type | smallint | NO |  |
| target_id | ARRAY | NO |  |
| target_id_user | integer | NO |  |
| trigger_id_user | integer | YES |  |
| event_type | text | NO |  |
| event_detail | json | YES |  |


## Table: `user_flag`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id_user | integer | NO |  |
| flag | text | NO |  |
| value | text | YES |  |


## Table: `user_info`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | NO | nextval('user_info_id_seq'::regclass) |
| uid | bigint | YES |  |
| name | text | NO |  |
| config | json | NO | '{}'::json |
| enable | boolean | NO | false |


## Table: `version_time`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO | nextval('version_time_version_seq'::regclass) |
| modified_time | bigint | NO |  |


## Table: `version_time_0`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO | nextval('version_time_0_version_seq'::regclass) |
| modified_time | bigint | NO |  |


## Table: `version_time_1`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO | nextval('version_time_1_version_seq'::regclass) |
| modified_time | bigint | NO |  |


## Table: `version_time_2`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO | nextval('version_time_2_version_seq'::regclass) |
| modified_time | bigint | NO |  |


## Table: `version_time_3`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| version | bigint | NO | nextval('version_time_3_version_seq'::regclass) |
| modified_time | bigint | NO |  |


## Table: `video`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| id | integer | YES |  |
| id_user | integer | YES |  |
| item_type | smallint | YES |  |
| type | smallint | YES |  |
| filename | text | YES |  |
| filesize | bigint | YES |  |
| createtime | bigint | YES |  |
| takentime | bigint | YES |  |
| mtime | bigint | YES |  |
| duplicate_hash | text | YES |  |
| cache_key | text | YES |  |
| resolution | json | YES |  |
| index_stage | smallint | YES |  |
| version | bigint | YES |  |
| id_item | integer | YES |  |
| id_folder | integer | YES |  |
| id_geocoding | integer | YES |  |
| is_major | boolean | YES |  |
| duration | bigint | YES |  |
| video_info | json | YES |  |
| audio_info | json | YES |  |


## Table: `video_additional`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| duration | bigint | NO |  |
| video_info | json | NO |  |
| audio_info | json | NO |  |
| id_unit | integer | YES |  |


## Table: `video_convert`

| Column Name | Data Type | Nullable | Default |
|-------------|-----------|----------|---------|
| duration | bigint | NO |  |
| quality | text | NO | ''::text |
| video_info | json | NO | '{}'::json |
| audio_info | json | NO | '{}'::json |
| id_unit | integer | YES |  |


