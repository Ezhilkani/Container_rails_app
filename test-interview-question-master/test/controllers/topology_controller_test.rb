require 'test_helper'

class TopologyControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get topology_index_url
    assert_response :success
  end

end
