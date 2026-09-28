Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Found 32 test(s).
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, auth, contenttypes, sessions, shipping
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying shipping.0001_initial...test_empty_order_400 (shipping.tests.test_api.OrderEndpointTests.test_empty_order_400) ... ok
test_order_recommendation (shipping.tests.test_api.OrderEndpointTests.test_order_recommendation) ... ok
test_unfittable_order_422 (shipping.tests.test_api.OrderEndpointTests.test_unfittable_order_422) ... ok
test_unknown_order_404 (shipping.tests.test_api.OrderEndpointTests.test_unknown_order_404) ... ok
test_bad_payloads_400 (shipping.tests.test_api.RecommendEndpointTests.test_bad_payloads_400) ... ok
test_duplicate_skus_are_merged (shipping.tests.test_api.RecommendEndpointTests.test_duplicate_skus_are_merged) ... ok
test_get_not_allowed (shipping.tests.test_api.RecommendEndpointTests.test_get_not_allowed) ... ok
test_inactive_box_is_never_recommended (shipping.tests.test_api.RecommendEndpointTests.test_inactive_box_is_never_recommended) ... ok
test_invalid_json_400 (shipping.tests.test_api.RecommendEndpointTests.test_invalid_json_400) ... ok
test_returns_cheapest_fitting_box (shipping.tests.test_api.RecommendEndpointTests.test_returns_cheapest_fitting_box) ... ok
test_rotation_case_via_api (shipping.tests.test_api.RecommendEndpointTests.test_rotation_case_via_api) ... ok
test_too_many_units_400 (shipping.tests.test_api.RecommendEndpointTests.test_too_many_units_400) ... ok
test_unknown_sku_400 (shipping.tests.test_api.RecommendEndpointTests.test_unknown_sku_400) ... ok
test_all_boxes_too_light_returns_none (shipping.tests.test_packing.RecommendBoxTests.test_all_boxes_too_light_returns_none) ... ok
test_cheaper_box_wins_even_if_bigger (shipping.tests.test_packing.RecommendBoxTests.test_cheaper_box_wins_even_if_bigger) ... ok
test_empty_items_raises (shipping.tests.test_packing.RecommendBoxTests.test_empty_items_raises) ... ok
test_exact_fit_is_accepted (shipping.tests.test_packing.RecommendBoxTests.test_exact_fit_is_accepted) ... ok
test_input_order_does_not_change_result (shipping.tests.test_packing.RecommendBoxTests.test_input_order_does_not_change_result) ... ok
test_item_too_big_for_every_box_returns_none (shipping.tests.test_packing.RecommendBoxTests.test_item_too_big_for_every_box_returns_none) ... ok
test_just_over_boundary_is_rejected (shipping.tests.test_packing.RecommendBoxTests.test_just_over_boundary_is_rejected) ... ok
test_multiple_items_packed_without_overlap (shipping.tests.test_packing.RecommendBoxTests.test_multiple_items_packed_without_overlap) ... ok
test_no_boxes_returns_none (shipping.tests.test_packing.RecommendBoxTests.test_no_boxes_returns_none) ... ok
test_rotation_allows_long_item (shipping.tests.test_packing.RecommendBoxTests.test_rotation_allows_long_item) ... ok
test_single_item_gets_cheapest_fitting_box (shipping.tests.test_packing.RecommendBoxTests.test_single_item_gets_cheapest_fitting_box) ... ok
test_tie_on_cost_prefers_smaller_volume_then_id (shipping.tests.test_packing.RecommendBoxTests.test_tie_on_cost_prefers_smaller_volume_then_id) ... ok
test_totals_reported (shipping.tests.test_packing.RecommendBoxTests.test_totals_reported) ... ok
test_volume_ok_but_shape_impossible (shipping.tests.test_packing.RecommendBoxTests.test_volume_ok_but_shape_impossible) ... ok
test_weight_limit_skips_box (shipping.tests.test_packing.RecommendBoxTests.test_weight_limit_skips_box) ... ok
test_try_pack_returns_none_when_full (shipping.tests.test_packing.TryPackTests.test_try_pack_returns_none_when_full) ... ok
test_bad_box_rejected (shipping.tests.test_packing.ValidationTests.test_bad_box_rejected) ... ok
test_negative_weight_rejected (shipping.tests.test_packing.ValidationTests.test_negative_weight_rejected) ... ok
test_zero_dimension_item_rejected (shipping.tests.test_packing.ValidationTests.test_zero_dimension_item_rejected) ... ok

----------------------------------------------------------------------
Ran 32 tests in 0.281s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
 OK
System check identified no issues (0 silenced).
