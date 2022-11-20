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
                <form action="/addPurchases" method="POST">
                    <div class="form-group">
                        <label>Warehouse Id : </label>
                        <input type="text" class="form-control" name="warehouseId" placeholder="Enter Warehouse Id" required><br>
                    </div>
                    <div class="form-group">
                        <label>Warehouse Location : </label>
                        <input type="text" class="form-control" name="warehouseName" placeholder="Enter Name" required><br>
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