var modelWrap = null;

const addWarehouse = () =>{

    if(modelWrap != null){
        modelWrap.remove();
    }

    console.log("Clicked");
    modelWrap = document.createElement('div');

    modelWrap.innerHTML = `
    <div class="modal">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h3 class="modal-title">Add Warehouse</h3>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
                <form action="/addWarehouse" method="POST">
                    <div class="form-group">
                        <label>Warehouse Name : </label>
                        <input type="text" class="form-control" name="warehouseName" placeholder="Enter Warehouse Name" required><br>
                    </div>
                    <div class="form-group">
                        <label>Warehouse Location : </label>
                        <input type="text" class="form-control" name="warehouseLocation" placeholder="Enter Location" required><br>
                    </div>
                    <div class="form-group">
                        <input class="btn btn-success" type="submit" value="Add">
                    </div>
                </form>
            </div>
          </div>
        </div>
    </div>
    `;

    document.body.append(modelWrap);

    var modal = new bootstrap.Modal(modelWrap.querySelector('.modal'));
    modal.show();
}