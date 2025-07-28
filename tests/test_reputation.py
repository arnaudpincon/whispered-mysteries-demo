# test_reputation_system.py
"""
Test script to verify the proper functioning of the reputation system
"""

def test_reputation_system():
    """Test the reputation system with correct thresholds"""
    from game_engine.core.game_state import GameState
    from game_engine.services.reputation_service import ReputationService
    
    # Initialize state and service
    state = GameState()
    state.current_location = "Main Hall"
    reputation_service = ReputationService(state)
    
    print("=== REPUTATION SYSTEM TEST ===\n")
    
    # Test 1: Impromptu actions in same room
    print("TEST 1: Impromptu Actions")
    print("Thresholds: Local=3, Global=6")
    
    for i in range(7):
        severity, game_over = reputation_service.process_nonsense_action(
            "impromptu", f"test_impromptu_{i+1}", "Main Hall"
        )
        status = reputation_service.get_reputation_status("Main Hall")
        
        local_status = "Main Hall" in state.impromptu_local_rooms
        global_status = state.is_impromptu_global
        room_count = status["room_counts"]["impromptu"]
        
        print(f"  Action {i+1}: Count={room_count}, Local={local_status}, Global={global_status}")
        
        # Check thresholds
        if i == 2:  # After 3rd action
            assert local_status == True, f"Should be local impromptu after 3 actions, got {local_status}"
        if i == 5:  # After 6th action
            assert global_status == True, f"Should be global impromptu after 6 actions, got {global_status}"
    
    print("Impromptu test passed!\n")
    
    # Reset for next test
    reputation_service.reset_reputation()
    
    # Test 2: Awkward actions in same room
    print("TEST 2: Awkward Actions")
    print("Thresholds: Local=2, Global=3")
    
    for i in range(4):
        severity, game_over = reputation_service.process_nonsense_action(
            "awkward", f"test_awkward_{i+1}", "Library"
        )
        status = reputation_service.get_reputation_status("Library")
        
        local_status = "Library" in state.awkward_local_rooms
        global_status = state.is_awkward_global
        room_count = status["room_counts"]["awkward"]
        
        print(f"  Action {i+1}: Count={room_count}, Local={local_status}, Global={global_status}")
        
        # Check thresholds
        if i == 1:  # After 2nd action
            assert local_status == True, f"Should be local awkward after 2 actions, got {local_status}"
        if i == 2:  # After 3rd action
            assert global_status == True, f"Should be global awkward after 3 actions, got {global_status}"
    
    print("Awkward test passed!\n")
    
    # Reset for next test
    reputation_service.reset_reputation()
    
    # Test 3: Dangerous actions in same room
    print("TEST 3: Dangerous Actions")
    print("Thresholds: Local=1, Global=2")
    
    for i in range(3):
        severity, game_over = reputation_service.process_nonsense_action(
            "dangerous", f"test_dangerous_{i+1}", "Drawing Room"
        )
        status = reputation_service.get_reputation_status("Drawing Room")
        
        local_status = "Drawing Room" in state.dangerous_local_rooms
        global_status = state.is_dangerous_global
        room_count = status["room_counts"]["dangerous"]
        
        print(f"  Action {i+1}: Count={room_count}, Local={local_status}, Global={global_status}, GameOver={game_over}")
        
        # Check thresholds
        if i == 0:  # After 1st action
            assert local_status == True, f"Should be local dangerous after 1 action, got {local_status}"
        if i == 1:  # After 2nd action
            assert global_status == True, f"Should be global dangerous after 2 actions, got {global_status}"
        if i == 2:  # After 3rd action (when already global)
            assert game_over == True, f"Should trigger game over when already global dangerous, got {game_over}"
    
    print("Dangerous test passed!\n")
    
    # Reset for next test
    reputation_service.reset_reputation()
    
    # Test 4: Different rooms don't affect each other
    print("TEST 4: Room Separation")
    
    # 1 dangerous action in Main Hall
    reputation_service.process_nonsense_action("dangerous", "test_1", "Main Hall")
    
    # 1 dangerous action in Library
    reputation_service.process_nonsense_action("dangerous", "test_2", "Library")
    
    # Should both be local dangerous but not global yet
    main_hall_local = "Main Hall" in state.dangerous_local_rooms
    library_local = "Library" in state.dangerous_local_rooms
    global_dangerous = state.is_dangerous_global
    
    print(f"  Main Hall local dangerous: {main_hall_local}")
    print(f"  Library local dangerous: {library_local}")
    print(f"  Global dangerous: {global_dangerous}")
    
    assert main_hall_local == True, "Main Hall should be local dangerous"
    assert library_local == True, "Library should be local dangerous"
    assert global_dangerous == False, "Should not be global dangerous yet (need 2 in same room)"
    
    # Now add second dangerous action in Main Hall - should trigger global
    reputation_service.process_nonsense_action("dangerous", "test_3", "Main Hall")
    global_dangerous = state.is_dangerous_global
    
    print(f"  After 2nd action in Main Hall - Global dangerous: {global_dangerous}")
    assert global_dangerous == True, "Should be global dangerous after 2 actions in same room"
    
    print("Room separation test passed!\n")
    
    # Test 5: Warning system
    print("TEST 5: Warning System")
    reputation_service.reset_reputation()
    
    # Test warnings at different thresholds
    reputation_service.process_nonsense_action("awkward", "test_1", "Dining Room")
    status = reputation_service.get_reputation_status("Dining Room")
    warnings = status["warnings"]
    
    print(f"  After 1 awkward action: {len(warnings)} warnings")
    print(f"    Warnings: {warnings}")
    
    # Should warn about next awkward action triggering local reputation
    assert any("local awkward" in warning.lower() for warning in warnings), "Should warn about local threshold"
    
    print("Warning system test passed!\n")
    
    print("ALL TESTS PASSED!")
    print("\nSystem summary:")
    print("• Impromptu: Local=3, Global=6")
    print("• Awkward: Local=2, Global=3") 
    print("• Dangerous: Local=1, Global=2")
    print("• Each room has its own local reputation")
    print("• Global = thresholds reached in ONE room")

if __name__ == "__main__":
    test_reputation_system()