var modelWrap = null;

const addStocks = () =>{

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
                  <h3 class="modal-title">Add Stocks</h3>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                    <form action="/addStocks" method="POST">
                        <div class="form-group">
                            <label>Stock Name : </label>
                            <input type="text" class="form-control" name="stockName" placeholder="Enter Stock Name" required><br>
                        </div>
                        <div class="form-group">
                            <label>Stock Quantity : </label>
                            <input type="text" class="form-control" name="qtyofstock" placeholder="Enter Stock Quantity" required><br>
                        </div>
                        <div class="form-group">
                            <label>Cost Price : </label>
                            <input type="text" class="form-control" name="costPrice" placeholder="Enter Cost Price" required><br>
                        </div>
                        <div class="form-group">
                            <label>Selling Price : </label>
                            <input type="text" class="form-control" name="sellingPrice" placeholder="Enter Selling Price" required><br>
                        </div>
                        <div class="form-group">
                            <label>Warehouse ID : </label>
                            <input type="text" class="form-control" name="warehouseId" placeholder="Enter Warehouse ID" required><br>
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


const editStocks = () =>{
    
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
              <h3 class="modal-title">Edit Stocks</h3>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
              <h3 class="modal-title">Stock ID : 4</h3>
            </div>
            <div class="modal-body">
                <form action="/editStocks" method="POST">
                    <div class="form-group">
                        <label>Stock Name : </label>
                        <input type ="hidden" value = "">
                        <input type="text" class="form-control"  name="stockName" placeholder="Enter Stock Name" value = "" required><br>
                    </div>
                    <div class="form-group">
                        <label>Stock Quantity : </label>
                        <input type="text" class="form-control" name="qtyofstock" placeholder="Enter Stock Quantity" value = "" required><br>
                    </div>
                    <div class="form-group">
                        <label>Cost Price : </label>
                        <input type="text" class="form-control" name="costPrice" placeholder="Enter Cost Price" value = "" required><br>
                    </div>
                    <div class="form-group">
                        <label>Selling Price : </label>
                        <input type="text" class="form-control" name="sellingPrice" placeholder="Enter Selling Price" value = "" required><br>
                    </div>
                    <div class="form-group">
                        <label>Warehouse ID : </label>
                        <input type="text" class="form-control" name="warehouseId" placeholder="Enter Warehouse ID" value = "" required><br>
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
