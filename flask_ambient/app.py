from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route("/")
def home():
    # names=[]
    # with open("files/names.txt", encoding="utf-8") as f:
    #     for raw_line in f:
    #         names.append(raw_line.strip())
    # print(names)
    # return "<br>".join(names)
    return render_template("index.html")


@app.route("/names")
def names():
    name = "Владимир"
    return render_template("names.html", name = name)

@app.route("/names2")
def names2():
    n = []
    with open("files/names.txt", encoding="utf-8") as f:
        for raw_line in f:
            n.append(raw_line.strip())


    return render_template("names2.html", n = n)

@app.route("/table")
def table():
    n = []
    with open("files/humans.txt", encoding="utf-8") as f:
        for raw_line in f:
            data = raw_line.strip().split(";")
            n.append({"last_name":data[0],"name":data[1],"sername":data[2]})

    return render_template("tables.html", n = n)

@app.route("/users")
def user_list():
    n = []
    with open("files/users.txt", encoding="utf-8") as f:
        for raw_line in f:
            data = raw_line.strip().split(";")
            n.append({"nic_name":data[0],"last_name":data[1],"name":data[2],"sername":data[3], "birday":data[4],"tel":data[5]})

    return render_template("user.html", n = n)

@app.route("/users/<login>")
def user_value(login):
    item = None
    with open("files/users.txt", encoding="utf-8") as f:
        for raw_line in f:
            data = raw_line.strip().split(";")
            if login == data[0]:
                item = ({"nic_name": data[0], "last_name": data[1], "name": data[2], "sername": data[3], "birday": data[4],
                      "tel": data[5]})
                break
    if item == None:
        abort(404)
    return render_template("user_page.html", item=item)


# @app.route("/about")
# def about():
#     return ("О нас!")

if __name__ == "__main__":
    app.run(debug=True)