<script type="text/javascript">//<![CDATA[
$(function() {
    // Cache frequently used selectors
    const categoryRow = $("#budget_item_category_type__row");
    const unitCostRow = $("#budget_item_unit_cost__row");
    const monthlyCostRow = $("#budget_item_monthly_cost__row");
    const minuteCostRow = $("#budget_item_minute_cost__row");
    const megabyteCostRow = $("#budget_item_megabyte_cost__row");
    const costTypeSelect = $("select[name='cost_type']");

    // Default to One-time costs
    // Hide the Running Cost inputs
    monthlyCostRow.hide();
    minuteCostRow.hide();
    megabyteCostRow.hide();
            
    // When the Cost type changes:
	costTypeSelect.change(function() {
		// What is the new cost type?
        cost_type = $(this).val();
        if (cost_type==2) {
            // Hide the Category
            categoryRow.hide();
            // Hide the Unit Cost input
            unitCostRow.hide();
            // Show the Running Cost inputs
            monthlyCostRow.show();
            minuteCostRow.show();
            megabyteCostRow.show();
        } else if (cost_type==1) {
            // Hide the Running Cost inputs
            monthlyCostRow.hide();
            minuteCostRow.hide();
            megabyteCostRow.hide();
            // Show the Category & Unit Cost input
            categoryRow.show();
            unitCostRow.show();
        }
	})
    
    // Set unused values before submitting form
    $("input[type='submit']:last").click(function(event){
        // What is the final cost type?
        cost_type = costTypeSelect.val();
        if (cost_type==2) {
            // Set the Category
            $('#budget_item_category_type').val("Running Cost")
            // Set the Unit Cost input
            $('#budget_item_unit_cost').val('0.0')
        } else if (cost_type==1) {
            // Set the Running Cost inputs
            $('#budget_item_monthly_cost').val('0.0')
            $('#budget_item_minute_cost').val('0.0')
            $('#budget_item_megabyte_cost').val('0.0')
        }
        // Pass to RESTlike CRUD controller
        event.preventDefault();
        return false;
    })
});
//]]></script>
