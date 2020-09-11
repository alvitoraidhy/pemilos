from tortoise import Tortoise, run_async
import asyncclick as click
import os, getpass
import config, models

conf = config.classes[os.environ.get('ENV', 'development')]

async def init():
    await Tortoise.init(
        db_url=conf.DB_URL,
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

@click.command()
@click.argument('arg')
async def main(arg):
    await init()

    if arg == 'add-admin':
        name = input('Name: ')
        username = input('Username: ')
        password = getpass.getpass(prompt='Password: ', stream=None) 

        try:
            new_admin = models.Admin(
                name=name, username=username
            )
            new_admin.set_password(password)
            await new_admin.save()

            click.echo('Successfully added an admin account!')

        except Exception as e:
            click.echo('An error occurred: ' + repr(e))

    elif arg == 'remove-admin':
        username = input('Username: ')

        try:
            admin = await models.Admin.get(username=username)
            await admin.delete()

            click.echo('Successfully removed an admin account: ' + username)

        except Exception as e:
            click.echo('An error occurred: ' + repr(e))

    elif arg == 'list-admin':
        admins = await models.Admin.all()

        click.echo('List of all admins:')
        for admin in admins:
            click.echo('- {} ({})'.format(admin.username, admin.name))

    await Tortoise.close_connections()


if __name__ == "__main__":
    main(_anyio_backend="asyncio")
