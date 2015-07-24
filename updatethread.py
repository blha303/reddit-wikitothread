import praw, sys, json
print "Welcome! Getting reddit object..."
r = praw.Reddit('GDQ thread autoupdater by /u/suudo')
print "Setting oauth info..."
with open("auth.json") as f:
    auth = json.load(f)
r.set_oauth_app_info(**auth["login"])
print "Refreshing token..."
r.set_access_credentials(**r.refresh_access_information(auth["token"]))

joiner = "Game | Runner / Channel | Time / Link\r\n--|--|--|"

print "Getting posts... (edit the file to change)"
post = r.get_submission("https://www.reddit.com/comments/3efduj")
comment1 = r.get_submission("https://www.reddit.com/comments/3efduj/_/cteefuw").comments[0]
comment2 = r.get_submission("https://www.reddit.com/comments/3efduj/_/cteefxf").comments[0]
comment3 = r.get_submission("https://www.reddit.com/comments/3efduj/_/ctef36b").comments[0]
data = r.get_wiki_page("suudo", "sgdq2015").content_md

print "OK! Starting on post updates"

def splitter(md):
    outp = ""
    postnum = 1
    for line in md.split("\r\n"):
        if len(outp) > 9500:
            if postnum is 1:
                print "** Finished with first post! Pushing to reddit..."
                outp += u"\r\n\r\nContinued in " + comment1.permalink
                post.edit(outp)
                outp = joiner
                postnum = 2
                print "** Push successful! Starting on post 2..."
            elif postnum is 2:
                print "** Finished with second post! Pushing to reddit..."
                outp += u"\r\n\r\nContinued in " + comment2.permalink
                comment1.edit(outp)
                outp = joiner
                postnum = 3
                print "** Push successful! Starting on post 3..."
            elif postnum is 3:
                print "** Finished with third post! Pushing to reddit..."
                outp += u"\r\n\r\nContinued in " + comment3.permalink
                comment2.edit(outp)
                outp = joiner
                postnum = 4
                print "** Push successful! Starting on post 4..."
            elif postnum is 4:
                print "** Finished with fourth post! Pushing to reddit..."
#                outp += u"\r\n\r\nContinued in " + comment4.permalink
                comment3.edit(outp)
                outp = joiner
                postnum = 5
                print "** Push successful! Starting on post 5..."
            elif postnum is 5:
                print "We got a problem. Add more comments."
                sys.exit(2)
        if not outp:
            outp = line
        else:
            outp += u"\r\n" + line
        print line
    if outp:
        print "Finished with source page text, pushing remainder..."
        if postnum is 1:
            post.edit(outp)
        elif postnum is 2:
            comment1.edit(outp)
        elif postnum is 3:
            comment2.edit(outp)
        elif postnum is 4:
            comment3.edit(outp)
#        elif postnum is 5:
#            comment4.edit(outp)
    print "All done!"

if __name__ == "__main__":
    splitter(data)